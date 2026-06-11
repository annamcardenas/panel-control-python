import requests
import os
from pathlib import Path

# Cargar el archivo .env manualmente
env_path = Path(__file__).parent.parent / '.env'
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                key, value = line.split('=', 1)
                os.environ[key] = value

TOKEN = os.getenv('TELEGRAM_TOKEN', '')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')

def enviar_mensaje(texto):
    if not TOKEN or not CHAT_ID:
        print(f"⚠️ Telegram no configurado: TOKEN={'SÍ' if TOKEN else 'NO'}, CHAT_ID={'SÍ' if CHAT_ID else 'NO'}")
        return
    try:
        url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
        response = requests.post(url, json={
            'chat_id': CHAT_ID,
            'text': texto,
            'parse_mode': 'Markdown'
        }, timeout=5)
        if response.status_code != 200:
            print(f"Error Telegram: {response.status_code}")
    except Exception as e:
        print(f'Error Telegram: {e}')
