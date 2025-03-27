from langchain_core.runnables import RunnableConfig

class AppConfig:
    """Application configuration class."""

    LOCAL_MODELS_PATH = "./models"
    LLM_HOST_URL = "http://ollama:11434"
    CHROMA_SERVICE_NAME = "chromadb"
    CHROMA_PORT = 8000

    # Ajout de cette conf pour fixer l'erreur dans main.py
    LLM_STREAM_RUN_CONF: RunnableConfig = {
        "configurable": {
            "session_id": "default"
        }
    }

app_config = AppConfig()
