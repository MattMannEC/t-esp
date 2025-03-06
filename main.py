from flask import Flask, Response, request
from services.graph import graph
from tools.logger import logger
from flask import Flask
from http import HTTPStatus

from langchain_core.messages import AIMessageChunk
from langchain_core.globals import set_debug
from langchain_core.runnables import RunnableConfig

from sse.sse import format_sse
from sse.announcer import MessageAnnouncer

set_debug(False)

# Run app
app = Flask(__name__)

announcer = MessageAnnouncer()
logger.info("graph compiled")


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
