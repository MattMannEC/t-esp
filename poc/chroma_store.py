import chromadb
from langchain_chroma import Chroma
from chromadb import Collection, ClientAPI
from langchain_huggingface import HuggingFaceEmbeddings

# Create a client to connect to the ChromaDB server and collection
chroma_client: ClientAPI = chromadb.HttpClient(host='localhost', port=8000)
COLLECTION_NAME = "themis"
collection: Collection = chroma_client.get_or_create_collection(name=COLLECTION_NAME)
embeddings_model = HuggingFaceEmbeddings()
# Create a Chroma instance
chroma_store = Chroma(
    collection_name=COLLECTION_NAME,
    client=chroma_client,
    embedding_function=embeddings_model
)


