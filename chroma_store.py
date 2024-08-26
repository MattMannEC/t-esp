import chromadb
from langchain_chroma import Chroma
from chromadb import Collection, ClientAPI

# Create a client to connect to the ChromaDB server and collection
chroma_client: ClientAPI = chromadb.HttpClient(host='localhost', port=8000)
COLLECTION_NAME = "themis"
collection: Collection = chroma_client.get_or_create_collection(name=COLLECTION_NAME)

# Create a Chroma instance
chroma_store = Chroma(
    client=chroma_client,
    collection_name=COLLECTION_NAME
)


