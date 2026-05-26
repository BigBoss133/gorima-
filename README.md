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

## Utilizzo

```bash
python3 chat.py
```

## Struttura del progetto

```
gorima-/
├── chat.py                # Entry point principale
├── intelligence_engine.py # Motore di analisi
├── llm_client.py          # Client LLM
├── gorima_prompt.py       # Prompt specializzati
├── collector.py            # Raccolta dati web
├── hybrid_collector.py     # Raccolta dati ibrida
├── bandi_radar.py          # Monitoraggio bandi
├── distill_skills.py       # Distillazione competenze
├── data/
│   ├── skills/             # Dati competenze
│   ├── bandi/              # Dati bandi
│   └── web_source/         # Fonti web
└── requirements.txt
```

## Note

Il progetto funziona in **modalità demo** con dati offline pre-cached, senza necessità di connessione live.