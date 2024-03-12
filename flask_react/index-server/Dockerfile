# index-server/Dockerfile
FROM nikolaik/python-nodejs:python3.11-nodejs16-slim

# Existing ARG and ENV
ARG LLM_LOCAL_PORT=11434
ENV LLM_LOCAL_PORT=${LLM_LOCAL_PORT}

ARG INDEX_SERVER_PORT=5601
ENV INDEX_SERVER_PORT=${INDEX_SERVER_PORT}

ARG API_SERVER_PORT=5602
ENV API_SERVER_PORT=${API_SERVER_PORT}

# New ARG and ENV for additional configurations
ARG FRONTEND_SERVER_PORT=3000
ENV FRONTEND_SERVER_PORT=${FRONTEND_SERVER_PORT}

ARG JWT_SECRET_KEY=xyzxyzxyz
ENV JWT_SECRET_KEY=${JWT_SECRET_KEY}

# Handling JSON in ARG requires careful management. To pass JSON, it's often
# better to encode it as a string when building the Docker image and decode it within the application.
ARG JWT_USERS='{"username1": {"password": "password1", "role": "user", "index_id": "0"}}'
ENV JWT_USERS=${JWT_USERS}

ARG LLM_LOCAL_PROVIDER=ollama
ENV LLM_LOCAL_PROVIDER=${LLM_LOCAL_PROVIDER}

ARG LLM_LOCAL_BASE=llm
ENV LLM_LOCAL_BASE=${LLM_LOCAL_BASE}

ARG LLM_LOCAL_PORT=11434
ENV LLM_LOCAL_PORT=${LLM_LOCAL_PORT}

ARG LLM_LOCAL_MODEL=llama2
ENV LLM_LOCAL_MODEL=${LLM_LOCAL_MODEL}

ARG LLM_LOCAL_EMBEDDING_MODEL=BAAI/bge-small-en-v1.5
ENV LLM_LOCAL_EMBEDDING_MODEL=${LLM_LOCAL_EMBEDDING_MODEL}

ARG LLM_CLOUD_PROVIDER=groq
ENV LLM_CLOUD_PROVIDER=${LLM_CLOUD_PROVIDER}

ARG LLM_CLOUD_BASE=https://api.groq.com/openai/v1
ENV LLM_CLOUD_BASE=${LLM_CLOUD_BASE}

# Empty defaults for optional configurations
ARG LLM_CLOUD_PORT=
ENV LLM_CLOUD_PORT=${LLM_CLOUD_PORT}

ARG LLM_CLOUD_MODEL=mixtral-8x7b-32768
ENV LLM_CLOUD_MODEL=${LLM_CLOUD_MODEL}

ARG LLM_CLOUD_KEY=
ENV LLM_CLOUD_KEY=${LLM_CLOUD_KEY}

ARG LLM_CLOUD_EMBEDDING_MODEL=BAAI/bge-small-en-v1.5
ENV LLM_CLOUD_EMBEDDING_MODEL=${LLM_CLOUD_EMBEDDING_MODEL}


WORKDIR /app

# os setup
RUN apt-get update && apt-get install -y \
    netcat-openbsd \
 && rm -rf /var/lib/apt/lists/*

# python setup for llama-index and dependencies (flask)
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt && pip cache purge

# folders
COPY ./index/ ./index
COPY ./mnt/ ./mnt
COPY ./index_libs/ ./index_libs

# scripts
COPY ./api.py ./api.py
COPY ./index.py ./index.py
COPY ./launch_app.sh ./launch_app.sh

# supervisor
RUN mkdir -p /etc/supervisor/conf.d
COPY wait-for-port.sh /usr/local/bin/wait-for-port.sh
RUN chmod +x /usr/local/bin/wait-for-port.sh
COPY supervisord.conf /etc/supervisor/supervisord.conf

# run startup script
CMD ["sh", "launch_app.sh"]
EXPOSE $INDEX_SERVER_PORT $API_SERVER_PORT


