from tools.logger import logger
import chromadb
from chromadb.api import ClientAPI
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from classes.config import app_config

import torch

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


model = HuggingFaceEmbeddings(
    model_name="dangvantuan/french-embedding-LongContext",
    model_kwargs={"trust_remote_code": True, 'device': device},
)
from tools.logger import logger

# model = HuggingFaceEmbeddings(model_name=f"{app_config.LOCAL_MODELS_PATH}/sentence-transformers/all-mpnet-base-v2")

def get_chroma_with_collection(collection_name = "langchain", host: str = app_config.CHROMA_SERVICE_NAME) -> Chroma:
    chroma_client: ClientAPI = chromadb.HttpClient(host=host, port=app_config.CHROMA_PORT)
    logger.info(f"Using chroma version: {chroma_client.get_version()}")
    return Chroma(
        collection_name=collection_name,
        client=chroma_client,
        embedding_function=model,
    )
