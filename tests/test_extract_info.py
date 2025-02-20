import sys
from pathlib import Path
from typing import List
from tools.prompts import get_rag_summary_prompt
from langchain_ollama import ChatOllama

# Get the parent directory of the current script
parent_dir = Path(__file__).resolve().parent.parent

# Add the parent directory to sys.path
sys.path.append(str(parent_dir))

from langchain_chroma import Chroma
import pytest
from tools.chroma_store import get_chroma_with_collection
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.documents import Document
import pprint

from classes.config import app_config


@pytest.fixture
def themis_collection() -> Chroma:
    return get_chroma_with_collection("route_et_travail_20250213")


@pytest.fixture
def llm() -> ChatOllama:
    return ChatOllama(
        model="qwen2.5:14b",
        verbose=True,
        base_url=app_config.LLM_HOST_URL,
        temperature=0.2,
    )


def test_extract_info(themis_collection: Chroma, llm):
    queries = [
        (
            "Je suis cadre. Je dois aller à Paris pour le travail, pour un séminaire avec"
            " le client de l'entreprise où je travaille. Le trajet ajoute 5 heures à ma "
            "journée de travail. Mon employeur doit-il me payer ces heures ?"
        )
    ]

    for q in queries:
        context: List[Document] = themis_collection.similarity_search(q, 4)
        prompt = get_rag_summary_prompt(context, q)
        pprint.pprint(prompt)

        result = llm.invoke(prompt)
        pprint.pprint(result)
        assert result
        # assert isinstance(result[0], Document)
        # assert any(
        #     "Une concentration d'alcool dans le sang égale ou supérieure à 0,20 gramme par litre".replace(
        #         " ", ""
        #     )
        #     in doc.page_content.replace("\n", " ").replace(" ", "")
        #     for doc in result
        # )
        # assert any(
        #     " titulaire d'un permis de conduire soumis au délai probatoire".replace(
        #         " ", ""
        #     )
        #     in doc.page_content.replace("\n", " ").replace(" ", "")
        #     for doc in result
        # )

