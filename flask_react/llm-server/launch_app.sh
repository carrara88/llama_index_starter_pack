#!/bin/bash
export OLLAMA_HOST=0.0.0.0:$LLM_LOCAL_PORT
# start ollama (service)
ollama serve