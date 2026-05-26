import os
import json
import requests
from playwright.sync_api import sync_playwright
import trafilatura

# CONFIGURATION
DATA_DIR = '/home/mike/gorima_engine/data/bandi'
os.makedirs(DATA_DIR, exist_ok=True)

TARGET_SOURCES = {
    'anas': {
        'url': 'https://www.anas.it/cantiere/gare-e-appalti/', 
        'method': 'playwright', 
        'keywords': ['bitume', 'asfalto', 'pavimentazione', 'cam', 'conglomerato']
    },
    'sicilia_gare': {
        'url': 'https://www.regione.sicilia.it/', 
        'method': 'trafilatura', 
        'keywords': ['bandi', 'strade', 'pavimentazione', 'sicilia']
    }
}

def filter_content(text, keywords):
    if not text: return False
    return any(kw.lower() in text.lower() for kw in keywords)

def scrape_source():
    print('🚀 Starting Bandi Radar monitoring...')
    
    # Playwright for dynamic sites (ANAS)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        for source, cfg in TARGET_SOURCES.items():
            try:
                print(f'Monitoring {source}...')
                if cfg['method'] == 'playwright':
                    page.goto(cfg['url'], wait_until='networkidle')
                    content = page.content()
                    extracted = trafilatura.extract(content)
                else:
                    downloaded = trafilatura.fetch_url(cfg['url'])
                    extracted = trafilatura.extract(downloaded) if downloaded else None
                
                if extracted and filter_content(extracted, cfg['keywords']):
                    filename = f'{source}_latest.md'
                    with open(os.path.join(DATA_DIR, filename), 'w') as f:
                        f.write(extracted)
                    print(f'✅ Relevant tender found on {source}! Saved to {filename}')
                else:
                    print(f'⚪ No relevant updates on {source}.')
            except Exception as e:
                print(f'❌ Error monitoring {source}: {e}')
        
        browser.close()

if __name__ == '__main__':
    scrape_source()
