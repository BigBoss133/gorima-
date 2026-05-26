import requests
import json
import os
from urllib.parse import urljoin, urlparse

API_KEY = 'fc-9aa6be66caa24c4da2558599e4d2459b'
BASE_URL_API = 'https://api.firecrawl.dev/v1/crawl'
START_URL = 'https://www.gorima.it/'
OUTPUT_DIR = '/home/mike/gorima_engine/data/web_source'

def start_crawl():
    print(f'Starting deep crawl of {START_URL}...')
    payload = {
        'url': START_URL,
        'scrapeOptions': {
            'formats': ['markdown']
        }
    }
    headers = {'Authorization': f'Bearer {API_KEY}', 'Content-Type': 'application/json'}
    
    try:
        response = requests.post(BASE_URL_API, json=payload, headers=headers)
        if response.status_code == 200:
            job_id = response.json().get('id')
            print(f'Crawl started. Job ID: {job_id}')
            return job_id
        else:
            print(f'Error starting crawl: {response.status_code} - {response.text}')
            return None
    except Exception as e:
        print(f'Exception: {e}')
        return None

def check_status(job_id):
    status_url = f'https://api.firecrawl.dev/v1/crawl/{job_id}'
    headers = {'Authorization': f'Bearer {API_KEY}'}
    
    while True:
        response = requests.get(status_url, headers=headers)
        data = response.json()
        status = data.get('status')
        print(f'Current status: {status}...')
        
        if status == 'completed':
            return data.get('data', [])
        elif status == 'failed':
            print('Crawl failed.')
            return None
        
        import time
        time.sleep(5)

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    job_id = start_crawl()
    if job_id:
        results = check_status(job_id)
        if results:
            for item in results:
                url = item.get('url')
                markdown = item.get('markdown', '')
                if markdown:
                    # Create a safe filename from the URL
                    filename = url.replace('https://', '').replace('www.', '').replace('/', '_').replace('.it', '').strip('_') + '.md'
                    if not filename: filename = 'index.md'
                    with open(f'{OUTPUT_DIR}/{filename}', 'w', encoding='utf-8') as f:
                        f.write(markdown)
            print(f'Crawl completed. {len(results)} pages saved to {OUTPUT_DIR}.')
    else:
        print('Failed to initiate crawl.')

if __name__ == '__main__':
    main()
