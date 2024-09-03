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


