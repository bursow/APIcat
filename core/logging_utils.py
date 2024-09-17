import logging
import time

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def handle_rate_limiting(retry_after):
    logging.info(f"Rate limiting uygulanıyor, {retry_after} saniye bekleniyor...")
    time.sleep(retry_after)

def add_api_key(headers, api_key=None):
    if api_key:
        headers['Authorization'] = f'Bearer {api_key}'
    return headers

def validate_url(url):
    from urllib.parse import urlparse
    parsed = urlparse(url)
    return all([parsed.scheme, parsed.netloc])
