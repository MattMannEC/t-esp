from tools.logger import logger
import chromadb
from chromadb.api import ClientAPI
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from transformers import AutoModel
from config import app_config

from sentence_transformers import SentenceTransformer
from typing import List
from embeddings import CustomEmbeddings
from tools.logger import logger

model = HuggingFaceEmbeddings(model_name=f"{app_config.LOCAL_MODELS_PATH}/sentence-transformers/all-mpnet-base-v2")

def get_chroma_with_collection(collection_name, host: str = "chromadb") -> Chroma:
    chroma_client: ClientAPI = chromadb.HttpClient(host=host, port=8000)
    logger.info(f"Using chroma version: {chroma_client.get_version()}")
    return Chroma(
        collection_name=collection_name,
        client=chroma_client,
        embedding_function=model,
    )
