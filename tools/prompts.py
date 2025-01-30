from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    PromptTemplate,
)

rag_system_prompt = (
    "Vous êtes un assistant qui rend le droit français plus accessible au grand public. "
    "Utilisez les informations suivantes pour répondre à la question posée. "
    "L'exactitude est primordiale : si vous ne trouvez pas l'information dans le contexte "
    "fourni ou si la question manque de clarté, posez une question pour demander des précisions "
    "ou reformulez pour mieux comprendre. La réponse doit être en français et concise. "
    "Résumé de la conversation : {summary} "
    "<context> {context} </context>"
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
