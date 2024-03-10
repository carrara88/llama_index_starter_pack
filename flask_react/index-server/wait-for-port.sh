#!/bin/bash
set -a
. /app/.env
set +a
# Imposta la porta e l'host che vuoi controllare
PORT=$INDEX_SERVER_PORT
HOST=localhost
TIMEOUT=60 # Tempo massimo di attesa in secondi

echo "In attesa che la porta $PORT su $HOST sia in ascolto..."
print_progress_bar() {
    local duration=$1
    local elapsed=$2
    local size=50 # Larghezza della barra di progresso
    local percent=$((100*elapsed/duration))
    local filled=$((size*elapsed/duration))
    local empty=$((size-filled))
    printf "\r["
    printf "%${filled}s" '' | tr ' ' '#'
    printf "%${empty}s" '' | tr ' ' '-'
    printf "] %s%%" $percent
}
# Controlla ogni secondo se la porta è in ascolto, per un massimo di TIMEOUT secondi
for i in $(seq $TIMEOUT); do
    nc -z $HOST $PORT && echo "Porta $PORT è ora in ascolto." && exit 0
    print_progress_bar $TIMEOUT $i
    sleep 1
done

echo "Tempo scaduto: la porta $PORT non è in ascolto dopo $TIMEOUT secondi."
exit 1
