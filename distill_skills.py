import json
import os

# Configuration
GRAPH_FILE = '/home/mike/gorima_engine/graph_report.json'
SKILLS_DIR = '/home/mike/gorima_engine/data/skills'
os.makedirs(SKILLS_DIR, exist_ok=True)

def create_skill(name, content, tags):
    skill_path = os.path.join(SKILLS_DIR, f'{name.lower().replace(" ", "_")}.md')
    template = f"""# 🛡️ SKILL: {name}
## 🎯 Obiettivo: {tags}

{content}

---
*Generata automaticamente dal Gorima Intelligence Engine*
"""
    with open(skill_path, 'w', encoding='utf-8') as f:
        f.write(template)
    return skill_path

def distill():
    print("Distilling knowledge graph into operational skills...")
    with open(GRAPH_FILE, 'r') as f:
        graph = json.load(f)
    
    # Mock-distillation based on graph nodes (since we are in prototype phase)
    # In a real scenario, this would use an LLM to synthesize the 'content'
    # We will simulate the 'Genius' output based on the scraped data
    
    skills_to_create = [
        {
            "name": "Vantaggio Logistico Sicilia",
            "tags": "Logistica, Competitività, Catanzaro",
            "content": "Sfrutta il deposito di Catanzaro come hub strategico per ridurre i tempi di consegna e i costi di trasporto verso la Sicilia rispetto ai competitor del Nord Italia."
        },
        {
            "name": "Conformità CAM 2025",
            "tags": "Normativa, Sostenibilità, Punteggi",
            "content": "Utilizza le tecnologie green (WMA e polverino di gomma) per massimizzare i punteggi premianti nei bandi ANAS aggiornati a Settembre 2025."
        },
        {
            "name": "Approccio Babbu Sutta u Lenzulu",
            "tags": "Strategia di Vendita, Psicologia Cliente",
            "content": "Identifica il profilo del cliente che finge ingenuità per ottenere sconti. Rispondi con valore tecnico e fermezza sui costi, spostando l'attenzione dal prezzo alla qualità della durata stradale."
        }
    ]
    
    for s in skills_to_create:
        path = create_skill(s['name'], s['content'], s['tags'])
        print(f'Skill created: {path}')

if __name__ == '__main__':
    distill()
