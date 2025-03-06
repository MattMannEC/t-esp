
from langchain_ollama import ChatOllama
from langchain_core.runnables import RunnableConfig
from classes.config import app_config


stream_config: RunnableConfig = {"metadata": {"stream": True}}
llm_for_streaming = ChatOllama(
    model="qwen2.5:14b", verbose=True, base_url=app_config.LLM_HOST_URL, temperature=0.2
).with_config(config=stream_config)


llm = ChatOllama(
    model="qwen2.5:14b", verbose=True, base_url=app_config.LLM_HOST_URL, temperature=0.2
)