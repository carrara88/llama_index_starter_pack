# server-ollama/Dockerfile
FROM nikolaik/python-nodejs:python3.11-nodejs16-slim

# load ARG from docker-composer.yml for BUILD
ARG LLM_LOCAL_PORT=11434
# set ENV as ARG for RUNTIME
ENV LLM_LOCAL_PORT=${LLM_LOCAL_PORT}

# load ARG from docker-composer.yml for BUILD
ARG LLM_LOCAL_MODEL=llama2
# set ENV as ARG for RUNTIME
ENV LLM_LOCAL_MODEL=${LLM_LOCAL_MODEL}

WORKDIR /app

# os setup
RUN apt-get update && apt-get install -y \
    curl \
    systemd \
    netcat-openbsd \
 && rm -rf /var/lib/apt/lists/*

# setup llm
RUN curl -fsSL https://ollama.com/install.sh | sh
# copy llm setup script
COPY ./setup_llm.sh ./setup_llm.sh
# setup llm (serve llm service and pull model image) (LLM_LOCAL_MODEL default is llama2)
RUN sh ./init_llm.sh

COPY ./launch_app.sh ./launch_app.sh
# run startup script
CMD ["sh", "launch_app.sh"]

EXPOSE $LLM_LOCAL_PORT
