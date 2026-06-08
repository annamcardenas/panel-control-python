import requests
import os

TOKEN = os.getenv('TELEGRAM_TOKEN', '')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')

def enviar_mensaje(texto):
    if not TOKEN or not CHAT_ID:
        return
    try:
        url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
        requests.post(url, json={
            'chat_id': CHAT_ID,
            'text': texto,
            'parse_mode': 'Markdown'
        }, timeout=5)
    except Exception as e:
        print(f'Error Telegram: {e}')
