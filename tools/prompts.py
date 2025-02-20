from typing import List
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    PromptTemplate,
)
from langchain_core.documents import Document

rag_system_prompt = (
    "Vous êtes un assistant juridique spécialisé dans le droit français, chargé de le rendre plus accessible au grand public. "
    "Votre objectif est de fournir des réponses précises, claires et concises basées exclusivement sur les informations disponibles. "
    "Si le contexte ne contient pas suffisamment d'informations pour répondre avec certitude, indiquez-le. "
    "L'exactitude est primordiale : ne faites aucune supposition et ne fournissez pas d'informations non vérifiées. "
    "\n\n### INSTRUCTIONS :\n"
    "1. **Répondez uniquement à partir du contexte fourni.** Si l'information demandée n'est pas disponible, dites-le explicitement.\n"
    "2. **Soyez factuel** Formulez des réponses claires et compréhensibles pour un public non expert.\n"
    "3. **Soyez concis.** La réponse doit être aussi courte que possible.\n"
    "\nRésumé de la conversation : {summary}\n"
    "<context> {context} </context>"
)


def get_rag_summary_prompt(context: List[Document], q: str) -> str:
    return ( 
            "Vous êtes un assistant juridique expert en droit français. Votre tâche est d’analyser les documents fournis et d’extraire "
            "uniquement les informations **essentielles** en rapport avec la requête utilisateur.\n\n"
            
            "### **INSTRUCTIONS :**\n"
            "- **Ne retenez que les informations strictement pertinentes.**\n"
            "- **Formatez la réponse en Markdown** avec un titre et une liste de points clés.\n"
            "- **Citez directement les articles de loi, arrêtés et jurisprudences pertinents.**\n"
            "- **Ne générez que le nombre de points clés réellement utiles (un seul si suffisant, plusieurs si nécessaire).**\n"
            "- **Supprimez toute information inutile ou redondante.**\n"
            "- **Si aucune information pertinente n'est trouvée, précisez-le.**\n\n"

            "### **CONTEXTE :**\n"
            f"{context}\n\n"

            "### **REQUÊTE UTILISATEUR :**\n"
            f"{q}\n\n"

            "### **FORMAT ATTENDU :**\n"
            "```markdown\n"
            "# {q}\n\n"
            "{% for point in points %}"
            "- **{{ point.title }}** : {{ point.description }} (Référence : {{ point.reference }}).\n"
            "{% endfor %}"
            "```"
        )


# contextualize_q_system_prompt = """
# Étant donné un historique de conversation et le dernier message de l'utilisateur,
# qui pourrait faire référence au contexte de cet historique,
# formulez un message autonome qui puisse être compris sans l'historique.
# Le message doit impérativement être en français.
# Ne répondez pas à la question ; reformulez simplement le message si nécessaire, ou renvoyez-le tel quel.
# """

# contextualize_q_prompt = ChatPromptTemplate.from_messages(
#     [
#         ("system", contextualize_q_system_prompt),
#         MessagesPlaceholder("messages"),
#         ("human", "{input}"),
#     ]
# )

# history_aware_retriever = create_history_aware_retriever(
#     llm, chroma_store.as_retriever(), contextualize_q_prompt
# )

rag_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", rag_system_prompt),
        MessagesPlaceholder("messages"),
        ("human", "{input}"),
    ]
)
