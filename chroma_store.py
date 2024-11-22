from langchain.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
import chromadb

# Configurez le modèle d'embedding
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

# Connectez-vous à Chroma
chroma_client = chromadb.HttpClient(host='localhost', port=8000)

# Créez une instance de Chroma
chroma_store = Chroma(
    collection_name="example_collection",
    chroma_client=chroma_client,
    embedding_function=embeddings
)
