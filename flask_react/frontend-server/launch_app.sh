#!/bin/bash

## backend
# 3001 serve express backend webserver for communication with index server
# assumes you've ran npm install already (dockerfile does this during build)
# cd backend && npm run build && serve -s build

## frontend
# 3000 serve react frontend webserver for communication with index server
# assumes you've ran npm install already (dockerfile does this during build)
cd frontend && npm run build && serve -s build
