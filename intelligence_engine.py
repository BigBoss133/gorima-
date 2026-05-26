from dotenv import load_dotenv
load_dotenv()

from gorima_prompt import build_system_prompt
from llm_client import query_llm


def generate_executive_response(query):
    system_prompt = build_system_prompt()
    response = query_llm(system_prompt, query)
    return response


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
        print('=' * 60)
