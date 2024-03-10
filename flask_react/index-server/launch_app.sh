#!/bin/bash
# This shebang line tells the system to execute this script with bash, ensuring bash-specific syntax is correctly interpreted.
# Start supervisor python scripts as processes ( api.py = api_as_service / index.py = index_as_service )
supervisord -c /etc/supervisor/supervisord.conf
#python index.py &
# Inform the user that the script is now waiting for the index server to be available on its designated port.
# The ${INDEX_SERVER_PORT} variable should be set in the environment and indicates the port the index server listens on.
#echo "waiting for index server on port: ${INDEX_SERVER_PORT}..."
# Wait for the index server to start listening on its port. This loop uses `nc` (netcat) to check if the port is open.
# It repeats every 1 second until a connection is successful, indicating the server is up and running.
#while ! nc -z localhost $INDEX_SERVER_PORT; do   
#  sleep 1 # Pause for 1 second before re-checking if the server is listening on the port.
#done

# Notify the user that the index server is successfully listening on its designated port.
#echo "index server is listenin on port: ${INDEX_SERVER_PORT}"

# Start the API server by executing the Python script `api.py`.
# This line is executed after the index server has been confirmed to be up and running.
#echo "API server starting..."
#python api.py