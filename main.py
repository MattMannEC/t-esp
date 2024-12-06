from flask import Flask, Response, jsonify, request
from tools.logger import logger
from flask import Flask
from http import HTTPStatus

from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from flask_sse import sse
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from chroma_store import get_chroma_with_collection
from langchain_ollama import ChatOllama
from langchain_core.runnables import Runnable
from flask_cors import CORS
from langchain_core.messages import AIMessage, HumanMessage, AIMessageChunk
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph
from langchain_core.globals import set_debug
from langchain_core.runnables import RunnableConfig
from config import app_config
set_debug(False)

# Run app
app = Flask(__name__)
CORS(app)  # Enable CORS for all origins
app.config["REDIS_URL"] = "redis://redis"
logger.info("Register blueprint")
app.register_blueprint(sse, url_prefix="/stream")

config: RunnableConfig = {"run_name": "interface_destined"}
llm = ChatOllama(
    model="mistral:latest", verbose=True, base_url=app_config.LLM_HOST_URL
).with_config(config=config)

themis_collection = get_chroma_with_collection("constitution-1958")

# TODO add summary and input to prompt
rag_system_prompt = """
Vous êtes un assistant qui rend le droit français plus accessible au grand public.
Utilisez les informations suivantes pour répondre à la question posée.
L'exactitude est primordiale : si vous ne trouvez pas l'information dans le contexte fourni, indiquez simplement que vous ne la connaissez pas.
La réponse doit être en français et concise.

Résumé de la conversation :
{summary}

<context>
{context}
</context>
"""

# contextualize_q_system_prompt = """
# Étant donné un historique de conversation et le dernier message de l'utilisateur,
# qui pourrait faire référence au contexte de cet historique,
# formulez un message autonome qui puisse être compris sans l'historique.
# Le message doit impérativement être en français.
# Ne répondez pas à la question ; reformulez simplement le message si nécessaire, ou renvoyez-le tel quel.
# """

# contextualize_q_prompt = ChatPromptTemplate.from_messages(
#     [
#         ("system", contextualize_q_system_prompt),
#         MessagesPlaceholder("messages"),
#         ("human", "{input}"),
#     ]
# )

# history_aware_retriever = create_history_aware_retriever(
#     llm, chroma_store.as_retriever(), contextualize_q_prompt
# )

rag_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", rag_system_prompt),
        MessagesPlaceholder("messages"),
        ("human", "{input}"),
    ]
)

qa_chain: Runnable = create_stuff_documents_chain(llm, rag_prompt)
# rag_chain: Runnable = create_retrieval_chain(history_aware_rag_retriever, qa_chain)
rag_chain: Runnable = create_retrieval_chain(themis_collection.as_retriever(), qa_chain)

from langgraph.graph import StateGraph
from data_types import State
from tools.summarize import invoke_summary_model


def summarize(state: State):
    logger.info("summarize")
    """Retrieve information related to a query."""
    state["messages"].append(HumanMessage(state["input"]))
    if len(state["messages"]) < 3:
        return state
    response = invoke_summary_model(state)
    logger.info(f"summarized input : {response.content}")
    state["summary"] = response.content
    return state


def retrieve(state: State):
    logger.info("retrieve")
    """Retrieve information related to a query."""
    q = state.get("summary", state["input"])
    logger.info(f"Simimarity search on : {q}")
    retrieved_docs = themis_collection.similarity_search(
        q, k=1
    )
    state["context"] = retrieved_docs
    return state


def invoke_rag(state: State) -> State:
    logger.info("invoke_rag")
    state["summary"] = state.get("summary", "")
    response = rag_chain.invoke(state)
    logger.info(response)
    state["messages"].append(AIMessage(response["answer"]))
    return state


graph_builder = StateGraph(state_schema=State)
graph_builder.set_entry_point("summarize")
graph_builder.add_node(summarize)
graph_builder.add_node(retrieve)
graph_builder.add_node(invoke_rag)
graph_builder.add_edge("summarize", "retrieve")
graph_builder.add_edge("retrieve", "invoke_rag")
graph_builder.set_finish_point("invoke_rag")
memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)

logger.info("graph compiled")
@app.route("/simulate_llm")
async def simulate_llm() -> Response:
    prompt = request.args.get("prompt")
    if not prompt:
        return Response("Missing 'prompt' parameter", HTTPStatus.BAD_REQUEST)

    # docs = conditions_collection.similarity_search(prompt)
    config: RunnableConfig = {"configurable": {"thread_id": "abc1235"}}
    try:

        async for event in graph.astream_events(
            {"input": prompt},
            config=config,
            version="v1",
            include_names=["interface_destined"],
            debug=True,
        ):
            if isinstance(event.get("data").get("chunk"), AIMessageChunk):
                sse.publish({"message": event.get("data").get("chunk").content})

    except Exception as e:
        logger.error(e)
        return jsonify(error="Resource not found"), 404

    return Response("", HTTPStatus.OK)
