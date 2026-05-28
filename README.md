# 🛡️ Gorima Intelligence Engine

Motore di business intelligence per Gorima S.p.A. — raccoglie, analizza e sintetizza dati su bandi, competenze e mercato per supportare le decisioni aziendali.

## Prerequisiti

- Python 3.10+
- Dipendenze elencate in `requirements.txt`

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install
```

## Configurazione

Copiare il file di esempio e inserire le proprie chiavi API:

```bash
cp .env.example .env
```

Modificare `.env` con le API key necessarie. Non condividere il file `.env`.

**Chiavi supportate:**
- `GROQ_API_KEY` — obbligatoria, provider LLM primario
- `FIRECRAWL_API_KEY` — opzionale, per raccolta dati web

## Utilizzo

### 🖥️ Web App (Production Ready)

L'engine serve nativamente sia le interfacce statiche che le API tramite FastAPI.

```bash
./start_engine.sh
```

Apri `http://<IP>:8080/` nel browser.

### 💬 Chat CLI

```bash
python3 chat.py
```

### 🔌 API Server standalone

L'API e il web server sono ora unificati:
```bash
uvicorn api_server:app --port 8080
# POST http://localhost:8080/api/query {"query": "..."}
```

## Stack LLM

| Provider | Ruolo | Note |
|----------|-------|------|
| **Groq** | Primario | API key obbligatoria, latenza bassa |
| **Ollama** | Fallback | Solo su nodo con GPU (RTX 4060 Ti), modello `llama3.1:8b` |

Fallback automatico: Groq → Ollama locale → messaggio errore italiano.

## Struttura del progetto

```
gorima-/
├── engine.html            # Web app mobile-first (single file)
├── api_server.py          # Bridge HTTP per LLM (POST /api/query)
├── start_engine.sh        # Script avvio web app + API
├── chat.py                # Chat CLI interattiva
├── intelligence_engine.py # Motore di analisi
├── llm_client.py          # Client LLM (Groq → Ollama fallback)
├── gorima_prompt.py       # Prompt specializzati + caricamento skills
├── collector.py            # Raccolta dati web
├── hybrid_collector.py    # Raccolta dati ibrida
├── bandi_radar.py         # Monitoraggio bandi
├── distill_skills.py      # Distillazione competenze
├── data/
│   ├── skills/            # Dati competenze (.md, caricati automaticamente)
│   ├── bandi/             # Dati bandi
│   └── web_source/        # Fonti web
└── requirements.txt
```

## Web App — Funzionalità

- **Risposte keyword-based** per CAM/bandi, prezzi, concorrenza, prodotti, cliente babbù
- **Stimatore Cantiere** — 6 passi → report preliminare con calcoli
- **Fallback LLM** via `api_server.py` per domande complesse
- **Sidebar** con 6 ricerche frequenti
- **Mobile responsive** — sidebar collassabile su < 768px
- **Nessuna persistenza** — ogni refresh resetta la chat


## Docker (Consigliato per Produzione)

Il progetto include `Dockerfile` e `docker-compose.yml` per un facile deploy.

```bash
docker-compose up -d --build
```

L'applicazione sarà disponibile su `http://localhost:8080`.

## Deploy su nodo remoto


```bash
scp engine.html api_server.py start_engine.sh mike@mikes.local:~/gorima_engine/
ssh mike@mikes.local
cd ~/gorima_engine && ./start_engine.sh
```

## Note

Il progetto funziona in **modalità demo** con dati offline pre-cached, senza necessità di connessione live. Le skills vengono caricate automaticamente da `data/skills/*.md`.