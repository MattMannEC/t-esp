# How to run the POC on linux

## Pre-requisites
A linux distribution (or WSL)
Docker with docker compose
A python envrionnement setup for python 3.11.9 (ideally using [pyenv](https://github.com/pyenv/pyenv))

## To locally host an LLM Install Ollama
https://github.com/ollama/ollama/blob/main/README.md#quickstart

`curl -fsSL https://ollama.com/install.sh | sh`

`ollama pull MODEL_NAME`

`ollama serve`

## Install python packages
`cd POC_DIR`

`pip install -r requirements.txt`

## Compose database container
`docker compose up`

## Load documents into vector store
Run poc/rag.ipynb making sure to have a pdf document to store and configuring the path at `file_path`

## Run gunicorn server
`cd DIR_CONTAINING_MAIN.PY`
`gunicorn main:app --worker-class gevent --bind 127.0.0.1:8001`

## Run the RAG system
Connect to the event source in a navigator
`http://127.0.0.1:8001/`

Call the endpoint that starts the RAG system to send events
`http://127.0.0.1:8001/simulate_llm`





