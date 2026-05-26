import json
import os
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from dotenv import load_dotenv

load_dotenv()

from intelligence_engine import generate_executive_response


class APIHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        if self.path != "/api/query":
            self.send_response(404)
            self.end_headers()
            return
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            data = json.loads(body)
            query = data.get("query", "").strip()
            if not query:
                self._send_json({"response": "Query vuota.", "status": "error"}, 400)
                return
            response = generate_executive_response(query)
            self._send_json({"response": response, "status": "ok"}, 200)
        except json.JSONDecodeError:
            self._send_json({"response": "JSON non valido.", "status": "error"}, 400)
        except Exception as e:
            self._send_json({"response": f"Errore durante l'elaborazione: {str(e)}", "status": "error"}, 500)

    def _send_json(self, data, code):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def log_message(self, format, *args):
        pass


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), APIHandler)
    print(f"🛡️  Gorima API Server avviato su http://0.0.0.0:{port}")
    print(f"   Endpoint: POST /api/query")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server arrestato.")
        server.server_close()