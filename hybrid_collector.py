import os
import json
import requests
import trafilatura
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()

API_KEY_FIRECRAWL = os.getenv('FIRECRAWL_API_KEY', '')
DATA_DIR = '/home/mike/gorima_engine/data/web_source'
os.makedirs(DATA_DIR, exist_ok=True)

TARGETS = {
    'gorima.it': {'method': 'trafilatura', 'urls': ['https://www.gorima.it/']},
    'anas.it': {'method': 'playwright', 'urls': ['https://www.anas.it/']},
    'siteb.it': {'method': 'trafilatura', 'urls': ['https://www.siteb.it/']},
}

def scrape_trafilatura(url):
    print(f'Using Trafilatura for {url}...')
    downloaded = trafilatura.fetch_url(url)
    if downloaded:
        return trafilatura.extract(downloaded)
    return None

def scrape_playwright(url):
    print(f'Using Playwright for {url}...')
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until='networkidle')
        content = page.content()
        browser.close()
        return trafilatura.extract(content)

def scrape_firecrawl(url):
    print(f'Using Firecrawl for {url}...')
    api_url = f'https://api.firecrawl.dev/v1/scrape'
    payload = {'url': url, 'formats': ['markdown']}
    headers = {'Authorization': f'Bearer {API_KEY_FIRECRAWL}', 'Content-Type': 'application/json'}
    response = requests.post(api_url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json().get('data', {}).get('markdown', '')
    return None

def run():
    for domain, config in TARGETS.items():
        for url in config['urls']:
            filename = url.replace('https://', '').replace('/', '_') + '.md'
            filepath = os.path.join(DATA_DIR, filename)
            
            content = None
            method = config['method']
            
            try:
                if method == 'trafilatura':
                    content = scrape_trafilatura(url)
                elif method == 'playwright':
                    content = scrape_playwright(url)
                
                if not content:
                    content = scrape_firecrawl(url)
                
                if content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f'Successfully saved {url} to {filename}')
                else:
                    print(f'Failed to extract content from {url}')
            except Exception as e:
                print(f'Error scraping {url}: {e}')

if __name__ == '__main__':
    run()
