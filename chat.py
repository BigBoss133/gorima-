import os
import glob
from dotenv import load_dotenv
from intelligence_engine import generate_executive_response

load_dotenv()

def clear_screen():
    os.system('clear')

def check_api_keys():
    groq = os.getenv('GROQ_API_KEY', '').strip()
    openrouter = os.getenv('OPENROUTER_API_KEY', '').strip()
    if not groq and not openrouter:
        print('\x1b[91m❌ ERRORE: Nessuna API key configurata.\x1b[0m')
        print('Imposta GROQ_API_KEY o OPENROUTER_API_KEY nel file .env')
        print('Copia .env.example in .env e inserisci le tue chiavi.')
        return False
    providers = []
    if groq:
        providers.append('Groq')
    if openrouter:
        providers.append('OpenRouter')
    print(f'\x1b[92m✅ Provider attivi: {", ".join(providers)}\x1b[0m')
    return True

def check_skills():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    skills_dir = os.path.join(base_dir, 'data', 'skills')
    skills = glob.glob(os.path.join(skills_dir, '*.md'))
    if not skills:
        print('\x1b[93m⚠️  Nessuna skill trovata in data/skills/\x1b[0m')
    else:
        print(f'\x1b[92m📚 {len(skills)} skill caricate\x1b[0m')
    return skills

def show_status():
    groq = os.getenv('GROQ_API_KEY', '').strip()
    openrouter = os.getenv('OPENROUTER_API_KEY', '').strip()
    print('\n\x1b[96m📊 STATO SISTEMA\x1b[0m')
    print(f'  Groq:        {"\x1b[92m✅ Configurato\x1b[0m" if groq else "\x1b[91m❌ Non configurato\x1b[0m"}')
    print(f'  OpenRouter:  {"\x1b[92m✅ Configurato\x1b[0m" if openrouter else "\x1b[91m❌ Non configurato\x1b[0m"}')
    base_dir = os.path.dirname(os.path.abspath(__file__))
    skills_dir = os.path.join(base_dir, 'data', 'skills')
    skills = glob.glob(os.path.join(skills_dir, '*.md'))
    print(f'  Skill:       {len(skills)} caricate')
    print()

def show_skills():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    skills_dir = os.path.join(base_dir, 'data', 'skills')
    skills = glob.glob(os.path.join(skills_dir, '*.md'))
    if not skills:
        print('\n\x1b[93m⚠️  Nessuna skill trovata.\x1b[0m')
        return
    print('\n\x1b[96m📚 SKILL DISPONIBILI\x1b[0m')
    for skill_path in sorted(skills):
        name = os.path.splitext(os.path.basename(skill_path))[0].replace('_', ' ').title()
        print(f'  • {name}')
    print()

def start_chat():
    clear_screen()
    print('\x1b[95m' + '='*60)
    print('  🛡️  GORIMA INTELLIGENCE ENGINE - EXECUTIVE INTERFACE')
    print('  Status: ONLINE | Node: SURFACE | Context: GORIMA S.p.A.')
    print('='*60 + '\x1b[0m')

    if not check_api_keys():
        return

    check_skills()

    print('\nSistemi pronti. Posso aiutarti con l\'analisi dei bandi, la strategia commerciale o la conformità tecnica.')
    print('Comandi speciali: !status, !skills, exit\n')

    while True:
        try:
            user_input = input('\x1b[94m👤 Michele > \x1b[0m')
        except (EOFError, KeyboardInterrupt):
            print('\n\x1b[90mSpegno i sistemi... Arrivederci, Michele.\x1b[0m')
            break

        if user_input.lower() in ['exit', 'quit', 'esci']:
            print('\n\x1b[90mSpegno i sistemi... Arrivederci, Michele.\x1b[0m')
            break

        if not user_input.strip():
            continue

        if user_input.strip() == '!status':
            show_status()
            continue

        if user_input.strip() == '!skills':
            show_skills()
            continue

        print('\n\x1b[93m[ la AI sta analizzando il Grafo e le Skill... ]\x1b[0m')

        try:
            response = generate_executive_response(user_input)
        except Exception as e:
            response = f'\x1b[91mErrore durante l\'elaborazione: {str(e)}\x1b[0m'

        print('\n\x1b[92m🤖 GORIMA GENIUS:\x1b[0m')
        print(response)
        print('\n' + '-'*60)

if __name__ == '__main__':
    start_chat()