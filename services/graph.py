from tools.logger import logger

from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from tools.chroma_store import get_chroma_with_collection
from langchain_ollama import ChatOllama
from langchain_core.runnables import Runnable
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph
from langchain_core.globals import set_debug
from langchain_core.runnables import RunnableConfig
from classes.config import app_config
from tools.prompts import rag_prompt
from langgraph.graph import StateGraph
from classes.data_types import State
from tools.summarize import invoke_summary_model

set_debug(False)

config: RunnableConfig = app_config.LLM_STREAM_RUN_CONF
llm = ChatOllama(
    model="qwen2.5:14b", verbose=True, base_url=app_config.LLM_HOST_URL
).with_config(config=config)

themis_collection = get_chroma_with_collection("route_et_travail_20250213")


qa_chain: Runnable = create_stuff_documents_chain(llm, rag_prompt)
# rag_chain: Runnable = create_retrieval_chain(history_aware_rag_retriever, qa_chain)
rag_chain: Runnable = create_retrieval_chain(themis_collection.as_retriever(), qa_chain)


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
    retrieved_docs = themis_collection.similarity_search(q, k=3)
    if len(retrieved_docs) < 1:
        raise Exception("Node retrieve: similarity search didn't return any documents")
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
