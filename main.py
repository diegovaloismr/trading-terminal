import requests
import os

TOKEN = "8665085121:AAE8JtiaJSFfzUBzCXfkiE_Kj37PM-dZqdQ"
CHAT_ID = "1170473159"

def send_message(text):
    url = f"https://api.telegram.org/bot8665085121:AAE8JtiaJSFfzUBzCXfkiE_Kj37PM-dZqdQ/sendMessage"
    
    payload = {
        "chat_id": CHAT_ID,
        "text": text
    }

    response = requests.post(url, data=payload)
    return response.json()


if __name__ == "__main__":
    mensagem = """
🚀 RADAR WIN/WDO ONLINE

Sistema iniciado com sucesso.
"""
    send_message(mensagem)

