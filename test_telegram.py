import requests

TOKEN = '8864533695:AAFTMISxJeCs6kJKyzvz4Ww_zp-D0j37T0o'
CHAT_ID = '1576050223'

url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
response = requests.post(url, json={
    'chat_id': CHAT_ID,
    'text': 'Prueba'
}, timeout=5)
print(response.status_code)
print(response.json())
