from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from langchain.callbacks.manager import CallbackManager
from langchain_core.callbacks import StreamingStdOutCallbackHandler

callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

llm = Ollama(model="gemma:2b", callback_manager=callback_manager)

output_parser = StrOutputParser()
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a world class technical documentation writer."),
    ("user", "{input}")
])

chain = prompt | llm | output_parser

chain.invoke({"input": "how can langsmith help with testing?"})

