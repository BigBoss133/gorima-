import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

from intelligence_engine import generate_executive_response

app = FastAPI(title="Gorima API Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    response: str
    status: str

@app.post("/api/query")
def api_query(request: QueryRequest):
    query = request.query.strip()
    if not query:
        return JSONResponse(status_code=400, content={"response": "Query vuota.", "status": "error"})

    try:
        response = generate_executive_response(query)
        return {"response": response, "status": "ok"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"response": f"Errore durante l'elaborazione: {str(e)}", "status": "error"})

@app.get("/engine.html", response_class=HTMLResponse)
def serve_engine():
    try:
        with open("engine.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="engine.html not found")

@app.get("/", response_class=HTMLResponse)
def serve_root():
    return serve_engine()

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    print(f"🛡️  Gorima API Server avviato su http://0.0.0.0:{port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
