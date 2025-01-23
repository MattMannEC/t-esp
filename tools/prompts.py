
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain_core.globals import set_debug

set_debug(False)
# TODO add summary and input to prompt
rag_system_prompt = """
Vous êtes un assistant qui rend le droit français plus accessible au grand public.
Utilisez les informations suivantes pour répondre à la question posée.
L'exactitude est primordiale : si vous ne trouvez pas l'information dans le contexte fourni, indiquez simplement que vous ne la connaissez pas.
La réponse doit être en français et concise.

Résumé de la conversation :
{summary}

<context>
{context}
</context>
"""

rag_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", rag_system_prompt),
        MessagesPlaceholder("messages"),
        ("human", "{input}"),
    ]
)


summary_prompt = PromptTemplate(
    input_variables=["text", "max_length"],
    template=(
        "Vous êtes un assistant expert en rédaction. Votre tâche est de résumer "
        "le texte ci-dessous en français, de manière parfaitement claire, concise et fidèle au contenu. "
        "Le résumé ne doit pas dépasser {max_length} caractères. "
        "Assurez-vous d'écrire en français correct, sans fautes d'orthographe ni de grammaire, "
        "et de ne pas déformer le sens original.\n\n"
        "Texte à résumer :\n{text}\n\n"
        "Résumé (en {max_length} caractères maximum) :"
    )
)
