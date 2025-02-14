import sys
from pathlib import Path
from typing import List

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


@pytest.fixture
def themis_collection() -> Chroma:
    return get_chroma_with_collection("route_et_travail_20250213")


def test_similarity_search_permis_probatoire(themis_collection: Chroma):
    queries = [
        (
            "En France Métropolitain, avec un permis probatoire j'ai droit à combien de "
            "gramme d'alcool par litre de sang pour conduire ?"
        )
    ]

    for q in queries:
        result: List[Document] = themis_collection.similarity_search(q, 4)

        pprint.pprint(result)
        assert isinstance(result[0], Document)
        assert any(
            "Une concentration d'alcool dans le sang égale ou supérieure à 0,20 gramme par litre".replace(
                " ", ""
            )
            in doc.page_content.replace("\n", " ").replace(" ", "")
            for doc in result
        )
        assert any(
            " titulaire d'un permis de conduire soumis au délai probatoire".replace(
                " ", ""
            )
            in doc.page_content.replace("\n", " ").replace(" ", "")
            for doc in result
        )


def test_similarity_search_deplacement_exceptionnel(themis_collection: Chroma):
    queries = [
        (
            "Je suis cadre. Je dois aller à Paris pour le travail, pour un séminaire avec le"
            " client de l'entreprise où je travaille. Le trajet ajoute 5 heures à ma journée"
            " de travail. Mon employeur doit-il me payer ces heures ?"
        )
    ]
    for q in queries:
        result: List[Document] = themis_collection.similarity_search(q, 4)
        pprint.pprint(result)
        assert isinstance(result[0], Document)
        assert any(
            (
                "Le temps de déplacement professionnel pour se rendre sur le lieu d'exécution"
                " du contrat de travail n'est pas un temps de travail effectif. Toutefois,"
                " s'il dépasse le temps normal de trajet entre le domicile et le lieu habituel "
                "de travail, il fait l'objet d'une contrepartie soit sous forme de repos, soit"
                " sous forme financière. La part de ce temps de déplacement professionnel "
                "coïncidant avec l'horaire de travail n'entraîne aucune perte de salaire."
            ).replace(" ", "")
            in doc.page_content.replace("\n", " ").replace(" ", "")
            for doc in result
        )
