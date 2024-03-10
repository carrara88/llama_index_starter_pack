FROM nikolaik/python-nodejs:python3.11-nodejs16-slim

# load ARG from docker-composer.yml for BUILD
ARG FRONTEND_SERVER_PORT=3000
# set ENV as ARG for RUNTIME
ENV FRONTEND_SERVER_PORT=${FRONTEND_SERVER_PORT}

WORKDIR /app

# os setup
RUN apt-get update && apt-get install -y \
    netcat-openbsd \
 && rm -rf /var/lib/apt/lists/*

# setup frontend application
COPY . .
RUN cd frontend && npm install && npm install -g serve && cd .. 
RUN npm install -g supervisor

# run startup script
CMD ["sh", "launch_app.sh"]
EXPOSE $FRONTEND_SERVER_PORT
