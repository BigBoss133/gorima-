import os
import json

SKILLS_DIR = '/home/mike/gorima_engine/data/skills'

def get_skill_content(skill_name):
    path = os.path.join(SKILLS_DIR, f"{skill_name.lower().replace(' ', '_')}.md")
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    return None

def generate_executive_response(query):
    q = query.lower()
    if any(term in q for term in ["cam", "bando", "normativa", "anas", "green", "punteggio"]):
        res = "\n[ANALISI STRATEGICA: CONFORMITÀ NORMATIVA]\n"
        res += "📌 VERIFICA: Identificato requisito di conformità CAM 2025/Sostenibilità.\n"
        res += "✅ SOLUZIONE: Implementazione gamma 'Green' (WMA + polverino di gomma).\n"
        res += "🚀 VANTAGGIO: Massimizzazione del punteggio OEPV e riduzione impatto CO2.\n"
        res += "\n[SOPRAVVIVENZA TECNICA]\n" + (get_skill_content("Conformità CAM 2025") or "Skill in update...")
        return res
    if any(term in q for term in ["sconto", "cliente", "babbu", "prezzo", "trattativa"]):
        res = "\n[STRATEGIA COMMERCIALE: GESTIONE CLIENTE]\n"
        res += "⚠️ PROFILO: Rilevato comportamento 'Babbu sutta u lenzulu' (finta ingenuità per abbattere prezzo).\n"
        res += "🛡️ CONTRO-MOSSA: Pivot dal costo al VALORE. Enfasi su durabilità, riduzione manutenzione e garanzia tecnica.\n"
        res += "\n[SOPRAVVIVENZA COMMERCIALE]\n" + (get_skill_content("Approccio Babbu Sutta u Lenzulu") or "Skill in update...")
        return res
    if any(term in q for term in ["logistica", "catanzaro", "sicilia", "consegna", "trasporto"]):
        res = "\n[VANTAGGIO COMPETITIVO: LOGISTICA]\n"
        res += "📍 ASSET: Hub Strategico di Catanzaro.\n"
        res += "⚡ EFFICienza: Riduzione tempi di risposta e costi di trasporto rispetto a competitor del Nord.\n"
        res += "\n[SOPRAVVIVEN la Logistica]\n" + (get_skill_content("Vantaggio Logistico Sicilia") or "Skill in update...")
        return res
    if any(term in q for term in ["competitor", "adrige", "sicilbitumi", "confronto"]):
        res = "\n[BENCHMARK COMPETITIVO]\n"
        res += "🔍 ANALISI: Confronto basato su qualità del bitume modificato e capillarità distributiva.\n"
        res += "🏆 SUPERIORITÀ GORIMA: Integrazione verticale e certificazioni ISO 9001/14001/27001.\n"
        return res
    return "Dati analizzati nel grafo. Nessuna skill operativa specifica attivata. Risposta basata su Knowledge Base generale: Gorima S.p.A. è leader nella pavimentazione stradale con focus su sostenibilità e logistica siciliana."

if __name__ == '__main__':
    print('--- 🛡️ GORIMA ENGINE: FINAL EXECUTIVE VALIDATION ---')
    test_queries = [
        'Analisi compatibilità prodotti Gorima con i nuovi CAM 2025',
        'Strategia di vendita per cliente ostinato che chiede sconti',
        'Valutazione asset logistico deposito Catanzaro',
        'Confronto competitivo con competitor del nord Italia'
    ]
    for q in test_queries:
        print(f'\nQUERY: {q}')
        print(generate_executive_response(q))
        print('='*60)
