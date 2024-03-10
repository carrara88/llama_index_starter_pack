FROM nikolaik/python-nodejs:python3.11-nodejs16-slim

WORKDIR /app

# os setup
RUN apt-get update && apt-get install -y netcat-openbsd
# setup llama-index-embeddings (huggingface)
RUN pip install --no-cache-dir llama-index-embeddings-huggingface
# setup ollama service
RUN curl -fsSL https://ollama.com/install.sh | sh
# serve ollama service and pull model image llama2
RUN ollama serve & sleep 3; ollama pull llama2
# setup llama-index and dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt && pip cache purge 
RUN pip install transformers
RUN pip install llama-index-readers-file
RUN pip install llama-index-llms-ollama

# setup frontend application
COPY . .
RUN cd react_frontend && npm install && npm install -g serve && cd .. 

# run startup script
CMD ["sh", "launch_app.sh"]
EXPOSE 5601 3000
