import requests
import os

# Pobieramy z "Environment Variables" w PythonAnywhere
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

URL = "https://interwencjakryzysowa.pl/"
ERROR_PHRASE = "Error establishing a database connection"

def send_discord_notification(message: str):
    if not DISCORD_WEBHOOK_URL:
        print("❌ Brak ustawionego webhooka w zmiennych środowiskowych.")
        return
    try:
        r = requests.post(DISCORD_WEBHOOK_URL, json={"content": message})
        r.raise_for_status()
        print("✅ Powiadomienie wysłane.")
    except requests.exceptions.RequestException as e:
        print(f"❌ Błąd przy wysyłaniu powiadomienia: {e}")

def check_site():
    try:
        response = requests.get(URL, timeout=10)
        response.raise_for_status()
        if ERROR_PHRASE.lower() in response.text.lower():
            send_discord_notification(f"⚠️ Strona {URL} zwraca błąd bazy danych WordPressa!")
        else:
            print("✅ Strona działa poprawnie.")
            send_discord_notification(f"wszystko git")
    except requests.exceptions.RequestException as e:
        send_discord_notification(f"🚨 Strona {URL} jest niedostępna! Błąd: {e}")

if __name__ == "__main__":
    check_site()
