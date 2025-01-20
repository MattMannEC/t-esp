class AppConfig:
    """Application configuration class."""
    
    LOCAL_MODELS_PATH = "./models"
    LLM_HOST_URL = "http://ollama:11434"
    LLM_STREAM_RUN_CONF = {"run_name": "interface_destined"}
    REDIS_URL = "redis://redis"
    CHROMA_SERVICE_NAME = "chromadb"
    CHROMA_PORT = 8000

app_config = AppConfig()