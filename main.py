from typing import Annotated, TypedDict, Sequence
from flask import Flask, Response, request
import logging
from flask import Flask
from http import HTTPStatus
from flask_sse import sse
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, StateGraph
from langgraph.graph.message import add_messages

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import (
    AIMessage,
    AIMessageChunk,
    HumanMessage,
    AIMessageChunk,
    BaseMessage,
)
from chroma_store import chroma_store
from langchain_ollama import ChatOllama
from langchain_core.runnables import Runnable
from flask_cors import CORS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Run app
app = Flask(__name__)
CORS(app)  # Enable CORS for all origins
app.config["REDIS_URL"] = "redis://localhost"
logger.info("Register blueprint")
app.register_blueprint(sse, url_prefix="/stream")

llm = ChatOllama(model="mistral:latest", verbose=True)


rag_system_prompt = """
Vous êtes un assistant qui rend le droit français plus accessible au grand public.
Utilisez les informations suivantes pour répondre à la question posée.
L'exactitude est primordiale : si vous ne connaissez pas la réponse, indiquez simplement que vous ne savez pas.
La réponse doit être en français et comporter au maximum 80 caractères.

<context>
{context}
</context>
"""
contextualize_q_system_prompt = """
Étant donné un historique de conversation et le dernier message de l'utilisateur, 
qui pourrait faire référence au contexte de cet historique, 
formulez un message autonome qui puisse être compris sans l'historique. 
Ne répondez pas à la question ; reformulez simplement le message si nécessaire, ou renvoyez-le tel quel."""

contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

history_aware_retriever = create_history_aware_retriever(
    llm, chroma_store.as_retriever(), contextualize_q_prompt
)

rag_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", rag_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

rag_chain: Runnable = create_stuff_documents_chain(llm, rag_prompt)
retrieval_chain = create_retrieval_chain(history_aware_retriever, rag_chain)


class State(TypedDict):
    input: str
    chat_history: Annotated[Sequence[BaseMessage], add_messages]
    context: str
    answer: str


def call_model(state: State) -> State:
    response = retrieval_chain.invoke(state)
    return {
        "chat_history": [
            HumanMessage(state["input"]),
            AIMessage(response["answer"]),
        ],
        "context": response["context"],
        "answer": response["answer"],
    }


workflow = StateGraph(state_schema=State)
workflow.add_edge(START, "model")
workflow.add_node("model", call_model)
memory = MemorySaver()
graph = workflow.compile(checkpointer=memory)


# Simulates receiving an http query from the crow api which invokes the LLM and
# send messages to the Event stream.
@app.route("/simulate_llm")
def simulate_llm():
    prompt = request.args.get("prompt")
    if not prompt:
        return Response("Missing 'prompt' parameter", HTTPStatus.BAD_REQUEST)
    config = {"configurable": {"thread_id": "abc123"}}

    logger.info(f"Received prompt: {prompt}")
    for message, metadata in graph.stream(
        {"input": prompt}, config=config, stream_mode="messages", debug=True
    ):
        if isinstance(message, AIMessageChunk):
            sse.publish({"message": message.content})
    return Response("", HTTPStatus.OK)
