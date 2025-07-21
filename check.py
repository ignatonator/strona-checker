import requests
from bs4 import BeautifulSoup
import os
PUSHBULLET_API_KEY = os.environ.get('PUSHBULLET_API_KEY')
if not PUSHBULLET_API_KEY:
    raise ValueError("PUSHBULLET_API_KEY nie został ustawiony jako zmienna środowiskowa")

def send_pushbullet_notification(title, body):
    data = {
        "type": "note",
        "title": title,
        "body": body
    }
    response = requests.post(
        'https://api.pushbullet.com/v2/pushes',
        json=data,
        headers={
            'Access-Token': PUSHBULLET_API_KEY,
            'Content-Type': 'application/json'
        }
    )
    if response.status_code != 200:
        print("Błąd powiadomienia:", response.text)

def check_site():
    try:
        response = requests.get('https://interwencjakryzysowa.pl', timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        body = soup.find('body', {'id': 'error-page'})
        if body:
            error_div = body.find('div', {'class': 'wp-die-message'})
            if error_div and 'Error establishing a database connection' in error_div.text:
                send_pushbullet_notification(
                    "Błąd strony interwencjakryzysowa.pl",
                    "Error establishing a database connection"
                )
            else:
                print("✅ Strona działa.")
        else:
            print("✅ Brak błędu bazy danych.")
    except Exception as e:
        print("⚠️ Błąd:", str(e))

check_site()
