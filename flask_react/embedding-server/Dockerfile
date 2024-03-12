FROM nikolaik/python-nodejs:python3.11-nodejs16-slim

WORKDIR /app

# os setup
RUN apt-get update && apt-get install -y netcat-openbsd
# setup llama-index-embeddings (huggingface)
COPY ./requirements.txt .
RUN pip install -r requirements.txt && pip cache purge 

# setup frontend application
COPY . .

# run startup script
CMD ["sh", "launch_app.sh"]
EXPOSE 5601
