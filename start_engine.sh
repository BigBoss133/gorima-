#!/bin/bash
# Avvia Gorima Engine: API server + web server
cd "$(dirname "$0")"

# Attiva virtualenv se esiste
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Carica variabili d'ambiente
export $(grep -v '^#' .env | xargs) 2>/dev/null

# Avvia API server in background
python3 api_server.py &
API_PID=$!
echo "🛡️  API server avviato su porta 8080 (PID: $API_PID)"

# Avvia web server per engine.html in background
python3 -m http.server 8000 --directory . &
WEB_PID=$!
echo "🌐 Web server avviato su porta 8000 (PID: $WEB_PID)"

# Mostra URL di accesso
LOCAL_IP=$(hostname -I | awk '{print $1}')
echo ""
echo "✅ Gorima Engine avviato!"
echo "   📱 Web app: http://${LOCAL_IP}:8000/engine.html"
echo "   🔌 API:     http://localhost:8080/api/query"
echo ""
echo "Premi Ctrl+C per arrestare entrambi i server"

# Attendi Ctrl+C
trap "kill $API_PID $WEB_PID 2>/dev/null; echo '🛑 Server arrestati.'; exit 0" INT TERM
wait