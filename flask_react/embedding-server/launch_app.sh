#!/bin/bash

echo "Embedding server starting..."
# start embedding
supervisord -c /etc/supervisor/supervisord.conf
