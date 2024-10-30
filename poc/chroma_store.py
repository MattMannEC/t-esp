import chromadb
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
chroma_client = chromadb.HttpClient(host='localhost', port=8000)

chroma_store = Chroma(
    collection_name="example_collection",
    client=chroma_client,
    embedding_function=embeddings)