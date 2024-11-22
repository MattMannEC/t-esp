from prefect import flow, task
from prefect.tasks import task_input_hash
from datetime import timedelta
from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.callbacks.manager import CallbackManager
from langchain_core.callbacks import StreamingStdOutCallbackHandler
from langchain_core.runnables import RunnablePassthrough
from langchain_chroma import Chroma  
from chroma_store import chroma_store

# Cache configurations 
cache_expiry = timedelta(minutes=10)

# Task to retrieve data from the Chroma vector database
@task(cache_key_fn=task_input_hash, cache_expiration=cache_expiry)
def retrieve_data(question: str):
    docs = chroma_store.similarity_search(question)
    return docs

# Task to process data using the RAG components
@task
def process_data(docs, question: str):
    # Initialize RAG model and components
    llm = Ollama(model="mistral:latest", verbose=True, callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]))
    output_parser = StrOutputParser()
    
    rag_prompt = ChatPromptTemplate.from_template(RAG_TEMPLATE)
    
    chain = (
        RunnablePassthrough.assign(context=lambda input: format_docs(input["context"]))
        | rag_prompt
        | llm
        | output_parser
    )
    
    result = chain.invoke({"context": docs, "question": question})
    return result

# Task to store synthesized data into Chroma or other storage
@task
def store_data(result):
    print(f"Storing result: {result}")
    chroma_store.store(result)

# Define the main Prefect flow
@flow(name="RAG Automated Workflow")
def rag_automated_workflow(question: str = "Je suis serveur dans un bar, est-ce que mon patron peut me forcer à faire des heures supp ?"):
    # Task executions
    docs = retrieve_data(question)
    synthesized_result = process_data(docs, question)
    store_data(synthesized_result)

# Run the workflow
if __name__ == "__main__":
    rag_automated_workflow()
