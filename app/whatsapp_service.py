# app/whatsapp_service.py
import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()

META_ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
WHATSAPP_API_URL = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"

def send_whatsapp_message(phone_number: str, message: str):
    """
    Sends a text message to a user's WhatsApp number.
    """
    headers = {
        "Authorization": f"Bearer {META_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    
    payload = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "text": {"body": message},
    }

    print(f"Sending message to {phone_number}: {message}")
    
    try:
        response = requests.post(WHATSAPP_API_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        
        print(f"Message sent successfully. Status code: {response.status_code}")
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"Error sending message: {e}")
        return None