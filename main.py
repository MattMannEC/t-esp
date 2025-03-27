from flask import Flask, Response, request
from langchain_ollama import ChatOllama
from services.graph import graph
from tools.logger import logger
from flask import Flask
from http import HTTPStatus

from langchain_core.messages import AIMessageChunk
from langchain_core.globals import set_debug
from threading import Lock
from langchain_core.runnables import RunnableConfig
from classes.config import app_config
from tools.prompts import summary_prompt

from sse.sse import format_sse
from sse.announcer import MessageAnnouncer

set_debug(False)

# Run app
app = Flask(__name__)

announcer = MessageAnnouncer()
logger.info("graph compiled")
config: RunnableConfig = app_config.LLM_STREAM_RUN_CONF
llm = ChatOllama(
    model="mistral:latest", verbose=True, base_url=app_config.LLM_HOST_URL
).with_config(config=config)

@app.after_request
def add_headers(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response


@app.route("/stream", methods=["GET"])
def listen():
    user_id = request.args.get("user_id")
    if not user_id:
        return Response("Missing 'user_id' parameter", HTTPStatus.BAD_REQUEST)

    def stream(client_addr):
        messages = announcer.listen(client_addr)  # returns a queue.Queue
        while True:
            msg = messages.get()  # blocks until a new message arrives
            yield msg

    return Response(stream(user_id), mimetype="text/event-stream")


@app.route("/invoke")
def invoke() -> Response:
    prompt = request.args.get("prompt")
    user_id = request.args.get("user_id")
    if not prompt:
        return Response("Missing 'prompt' parameter", HTTPStatus.BAD_REQUEST)

    if not user_id:
        return Response("Missing 'user_id' parameter", HTTPStatus.BAD_REQUEST)

    try:
        invoke_graph(prompt, user_id)

    except Exception as e:
        logger.error(e)
        return Response("", HTTPStatus.BAD_REQUEST)

    return Response("", HTTPStatus.OK)


def invoke_graph(prompt: str, user_id: str):
    config: RunnableConfig = {
        "configurable": {"thread_id": user_id},
    }

    for s, m in graph.stream(
        {"input": prompt},
        config=config,
        stream_mode="messages",
    ):
        if isinstance(s, AIMessageChunk) and m.get("stream") is True:
            announcer.announce(
                msg=format_sse(data=s.content),
                client_addr=user_id,
            )
# TODO the summarized input needs to be coherent with the rag system prompt.

@app.route("/summarize", methods=["POST"])
def summarize():
    llm_lock = Lock()
    try:
        if not llm_lock.acquire(blocking=False):
            return Response("Le LLM est actuellement occupé. Veuillez réessayer plus tard.", HTTPStatus.TOO_MANY_REQUESTS)

        data = request.json
        if not data or "text" not in data:
            return Response("Missing 'text' parameter in JSON body", HTTPStatus.BAD_REQUEST)

        text = data["text"]
        text = truncate_text(text)
        logger.info(text)
        if not text.strip():
            return Response("Text cannot be empty", HTTPStatus.BAD_REQUEST)

        summary = summarize_recursively(text)

        return {"summary": summary}
    except Exception as e:
        logger.error(f"Erreur dans /summarize : {str(e)}")
        return Response("Une erreur est survenue lors du traitement de votre requête.", HTTPStatus.INTERNAL_SERVER_ERROR)
    finally:
        llm_lock.release()


def summarize_recursively(text: str, max_length: int = 50) -> str:
    truncated_text = truncate_text(text)
    
    try:
        prompt = summary_prompt.format(text=truncated_text, max_length=max_length)
        response = llm.invoke(prompt)

        logger.debug(f"Réponse brute du LLM : {response}")

        if hasattr(response, "content"):
            summary = response.content.strip()
            logger.info(f"Résumé extrait : {summary}")
            return summary

        else:
            logger.error("Réponse inattendue du LLM, pas de 'content'")
            return text

    except Exception as e:
        logger.error(f"Erreur lors du résumé : {str(e)}")
        return "Une erreur est survenue lors du résumé."


def truncate_text(text: str) -> str:
    tokens = text.split()
    if len(tokens) > 1024:
        return " ".join(tokens[:1024])
    return text
