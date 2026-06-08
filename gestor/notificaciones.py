import requests

TOKEN = '8864533695:AAFTMISxJeCs6kJKyzvz4Ww_zp-D0j37T0o'
CHAT_ID = '1576050223'

def enviar_mensaje(texto):
    try:
        url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
        requests.post(url, json={
            'chat_id': CHAT_ID,
            'text': texto,
            'parse_mode': 'Markdown'
        }, timeout=5)
    except Exception as e:
        print(f'Error Telegram: {e}')
