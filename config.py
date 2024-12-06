class AppConfig:
    """Application configuration class."""
    
    LOCAL_MODELS_PATH = "./models"
    LLM_HOST_URL = "http://ollama:11434"
    LLM_STREAM_RUN_CONF = {"run_name": "interface_destined"}

app_config = AppConfig()