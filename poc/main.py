from flask import Flask, Response, request
import json
import time
import logging
from flask import Flask, render_template
from http import HTTPStatus
from flask_sse import sse
from langchain_core.output_parsers import SimpleJsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from chroma_store import chroma_store
from langchain.callbacks.manager import CallbackManager
from langchain_core.callbacks import StreamingStdOutCallbackHandler
from langchain_ollama import ChatOllama
from langchain_core.runnables import RunnablePassthrough

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Run app
app = Flask(__name__)
app.config["REDIS_URL"] = "redis://localhost"
logger.info("Register blueprint")
app.register_blueprint(sse, url_prefix='/stream')

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

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

# Create RAG chain
logger.info("Create RAG chain")
rag_prompt = ChatPromptTemplate.from_template(RAG_TEMPLATE)
llm = ChatOllama(model="mistral:latest", verbose=True)
chain = (
    RunnablePassthrough.assign(context=lambda input: format_docs(input["context"]))
    | rag_prompt
    | llm
)
logger.info("Chain loaded")

def run_rag(question):
    docs = chroma_store.similarity_search(question)
    logger.info(docs)
    logger.info("Running chain")
    return chain.stream({"context": docs, "question": question})

# Simulates a request being sent from the web interface to the crow web app
# and connecting the web interface to the Event Source.
@app.route('/')
def index():
    return render_template("index.html")

# Simulates receiving an http query from the crow api which invokes the LLM and
# send messages to the Event stream.
@app.route('/simulate_llm')
def simulate_llm():
    question = "Est-ce que je peux dormir pendant ma pause au travail ?"
    for s in run_rag(question):
        sse.publish({"message": s.content})
    return Response("", HTTPStatus.OK)



