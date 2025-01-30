from flask import Flask, Response, request
from services.graph import graph
from tools.logger import logger
from flask import Flask
from http import HTTPStatus

from flask_sse import sse
from flask_cors import CORS
from langchain_core.messages import AIMessageChunk
from langchain_core.globals import set_debug
from langchain_core.runnables import RunnableConfig
from classes.config import app_config

set_debug(False)

# Run app
app = Flask(__name__)
CORS(app)  # Enable CORS for all origins
app.config["REDIS_URL"] = app_config.REDIS_URL
logger.info("Register blueprint")
app.register_blueprint(sse, url_prefix="/stream")

logger.info("graph compiled")


@app.route("/invoke")
async def invoke() -> Response:
    prompt = request.args.get("prompt")
    user_id = request.args.get("user_id")
    if not prompt:
        return Response("Missing 'prompt' parameter", HTTPStatus.BAD_REQUEST)

    if not user_id:
        return Response("Missing 'user_id' parameter", HTTPStatus.BAD_REQUEST)

    # docs = conditions_collection.similarity_search(prompt)
    config: RunnableConfig = {"configurable": {"thread_id": user_id}}
    try:
        async for event in graph.astream_events(
            {"input": prompt},
            config=config,
            version="v1",
            include_names=["interface_destined"]
        ):
            if isinstance(event.get("data").get("chunk"), AIMessageChunk):
                sse.publish({"value": event.get("data").get("chunk").content})

    except Exception as e:
        logger.error(e)
        return Response("", HTTPStatus.BAD_REQUEST)

    return Response("", HTTPStatus.OK)
