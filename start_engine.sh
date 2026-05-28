#!/bin/bash
# Avvia Gorima Engine: API server (FastAPI) + static files
cd "$(dirname "$0")"

# Attiva virtualenv se esiste
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Carica variabili d'ambiente
export $(grep -v '^#' .env | xargs) 2>/dev/null

export PORT="${PORT:-8080}"

# Avvia API server in background
uvicorn api_server:app --host 0.0.0.0 --port $PORT &
API_PID=$!
echo "🛡️  Gorima Engine avviato su porta $PORT (PID: $API_PID)"

# Mostra URL di accesso
LOCAL_IP=$(hostname -I | awk '{print $1}')
echo ""
echo "✅ Gorima Engine avviato!"
echo "   📱 Web app (Local): http://localhost:$PORT/"
echo "   📱 Web app (Network): http://${LOCAL_IP}:$PORT/"
echo "   🔌 API:     http://localhost:$PORT/api/query"
echo ""
echo "Premi Ctrl+C per arrestare il server"

# Attendi Ctrl+C
trap "kill $API_PID 2>/dev/null; echo '🛑 Server arrestato.'" INT TERM
wait
