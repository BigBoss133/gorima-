import os
from intelligence_engine import generate_executive_response

def clear_screen():
    os.system('clear')

def start_chat():
    clear_screen()
    print('\x1b[95m' + '='*60)
    print('  🛡️  GORIMA INTELLIGENCE ENGINE - EXECUTIVE INTERFACE')
    print('  Status: ONLINE | Node: SURFACE | Context: GORIMA S.p.A.')
    print('='*60 + '\x1b[0m')
    print('\nSistemi pronti. Posso aiutarti con l\'analisi dei bandi, la strategia commerciale o la conformità tecnica.\n')
    print('👉 Digita la tua domanda o scrivi \'exit\' per chiudere la sessione.\n')

    while True:
        user_input = input('\x1b[94m👤 Michele > \x1b[0m')
        
        if user_input.lower() in ['exit', 'quit', 'esci']:
            print('\n\x1b[90mSpegno i sistemi... Arrivederci, Michele.\x1b[0m')
            break
            
        if not user_input.strip():
            continue

        print('\n\x1b[93m[ la AI sta analizzando il Grafo e le Skill... ]\x1b[0m')
        
        response = generate_executive_response(user_input)
        
        print('\n\x1b[92m🤖 GORIMA GENIUS:\x1b[0m')
        print(response)
        print('\n' + '-'*60)

if __name__ == '__main__':
    start_chat()
