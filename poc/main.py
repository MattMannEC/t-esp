from flask import Flask, Response, request
import json
from rag import run_rag
import time


from flask import Flask, render_template
from flask_sse import sse

app = Flask(__name__)
app.config["REDIS_URL"] = "redis://localhost"
app.register_blueprint(sse, url_prefix='/stream')

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from chroma_store import chroma_store
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


from langchain.callbacks.manager import CallbackManager
from langchain_core.callbacks import StreamingStdOutCallbackHandler
from langchain_community.llms import Ollama
from langchain_core.runnables import RunnablePassthrough

RAG_TEMPLATE = """
Vous êtes un assistant qui rend le droit français plus accessible au grand public.
Utilisez les informations suivantes pour répondre à la question posée.
L'exactitude est primordiale : si vous ne connaissez pas la réponse, indiquez simplement que vous ne savez pas.
La réponse doit être en français et comporter au maximum 80 caractères.

<context>
{context}
</context>

Répondez à la question suivante:

{question}"""

rag_prompt = ChatPromptTemplate.from_template(RAG_TEMPLATE)
llm = Ollama(model="mistral:latest", verbose=True, callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]))
chain = (
    RunnablePassthrough.assign(context=lambda input: format_docs(input["context"]))
    | rag_prompt
    | llm
    | StrOutputParser()
)
print("Chain loaded")

def run_rag(question):
    docs = chroma_store.similarity_search(question)
    print("Context loaded")

    # Run the chain
    print("Running chain")
    return chain.invoke({"context": docs, "question": question})


# def generate_llm_response():
#     result = run_rag("Je suis serveur dans un bar, est-ce que mon patron peut me forcer à faire des heures supp ?")
#     yield f"data: {json.dumps(result)}\n\n"

@app.route('/simulate_llm')
def simulate_llm():
    question = "Je suis serveur dans un bar, est-ce que mon patron peut me forcer à faire des heures supp ?"
    def generate():
        result = run_rag(question)
        yield f"data: {json.dumps(result)}\n\n"
    return Response(generate(), mimetype='text/event-stream')



