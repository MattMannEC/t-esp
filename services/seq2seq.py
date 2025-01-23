from langchain.schema import AIMessage, HumanMessage, BaseMessage
from langchain.prompts import StringPromptTemplate
from langchain_huggingface import HuggingFacePipeline
from transformers import pipeline
from dataclasses import dataclass


def convert_chat_history_to_string(chat_history: list[BaseMessage]) -> str:
    conversation = ""
    for message in chat_history:
        if isinstance(message, HumanMessage):
            conversation += f"Utilisateur : {message.content}\n"
        elif isinstance(message, AIMessage):
            conversation += f"IA : {message.content}\n"
    return conversation

def summarize_chat_history(chat_history: list[BaseMessage], prompt_template: StringPromptTemplate) -> str:
    summarization_pipeline = pipeline("summarization", model="google-t5/t5-small")
    llm = HuggingFacePipeline(pipeline=summarization_pipeline)

    summarization_chain = prompt_template | llm
    conversation = convert_chat_history_to_string(chat_history)
    return summarization_chain.invoke(input={"conversation": conversation})
