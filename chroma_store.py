import chromadb
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="dangvantuan/french-embedding-LongContext",
    model_kwargs={"trust_remote_code": True},
)
chroma_client = chromadb.HttpClient(host="localhost", port=8000)

chroma_store = Chroma(
    collection_name="themis", client=chroma_client, embedding_function=embeddings
)
