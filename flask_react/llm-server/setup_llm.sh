#!/bin/bash
# start ollama on background (service)
ollama serve & 
# wait for ollama startup
sleep 3; 
# pull LLM image
ollama pull $LLM_LOCAL_MODEL
# terminate ollama service
kill $!