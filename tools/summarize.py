from tools.logger import logger
from classes.data_types import State
from classes.config import app_config

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Configure logger

summary_model = ChatOllama(
    model="mistral:latest", verbose=True, base_url=app_config.LLM_HOST_URL
)

system_prompt = (
    "Résumer progressivement les lignes de conversation fournies, en ajoutant au résumé précédent pour retourner un nouveau résumé.\n\n"
    "EXEMPLE\n"
    "Résumé actuel :\n"
    "L'humain demande ce que l'IA pense de l'intelligence artificielle. L'IA pense que l'intelligence artificielle est une force positive.\n\n"
    "Nouvelles lignes de conversation :\n"
    "Humain : Pourquoi pensez-vous que l'intelligence artificielle est une force positive ?\n"
    "IA : Parce que l'intelligence artificielle aidera les humains à atteindre leur plein potentiel.\n\n"
    "Nouveau résumé :\n"
    "L'humain demande ce que l'IA pense de l'intelligence artificielle. L'IA pense que l'intelligence artificielle est une force positive parce qu'elle aidera les humains à atteindre leur plein potentiel.\n"
    "FIN DE L'EXEMPLE\n\n"
    "Résumé actuel :\n{summary}\n\n"
    "Nouvelles lignes de conversation :\n{messages}\n\n"
    "Nouveau résumé :"
)

prompt: ChatPromptTemplate = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

def invoke_summary_model(state: State):
    logger.info(invoke_summary_model)
    chain = prompt | summary_model
    state["summary"] = state.get("summary", "")

    if len(state["messages"]) < 3:
        # TODO add exception ?
        logger.error("Messages history must contain at least 3 messages to summarize")
        return {}
    return chain.invoke(state)

