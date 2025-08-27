import os
from fastapi import FastAPI, Request, HTTPException, Depends
from dotenv import load_dotenv
from sqlalchemy.orm import Session

from app import whatsapp_service
from . import services, llm_service
from .database import get_db

load_dotenv()
app = FastAPI()
VERIFY_TOKEN = os.getenv("META_VERIFY_TOKEN")

# A simple in-memory store for chat history.
# In production, we'd use a database like Redis.
chat_histories = {}

@app.get("/webhook")
async def verify_webhook(request: Request):
    """
    This endpoint is used by Meta to verify your webhook URL.
    It checks for a mode, a token, and a challenge.
    """
    # Get all the parameters first
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    # Check if all required parameters are present and the token is correct
    if mode == "subscribe" and token == VERIFY_TOKEN and challenge is not None:
        print("Webhook verified successfully!")
        # Only convert to int after confirming it's not None
        return int(challenge)
    else:
        # If any part is missing or incorrect, fail the verification
        print("Webhook verification failed.")
        raise HTTPException(status_code=403, detail="Verification failed")


@app.post("/webhook")
async def handle_messages(request: Request, db: Session = Depends(get_db)):
    body = await request.json()
    print("Received raw webhook:", body)

    try:
        # Extract user message and phone number
        phone_number = body['entry'][0]['changes'][0]['value']['messages'][0]['from']
        user_message = body['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
        
        # Get or create the customer
        customer = services.get_or_create_customer(db, phone_number)

        # Retrieve or initialize chat history
        if customer.phone_number not in chat_histories:
            chat_histories[customer.phone_number] = [
                {"role": "system", "content": "You are a friendly and helpful salon booking assistant named 'Glossy'. The current date is August 27, 2025. The salon's available services are: Men's Haircut. The only available staff member is Sarah."},
            ]
        
        # RUN THE CONVERSATION
        assistant_response = llm_service.run_conversation(
            db=db,
            conversation_history=chat_histories[customer.phone_number],
            user_message=user_message,
            customer_phone=str(customer.phone_number)
        )
        
        print(f"💬 Assistant response: {assistant_response}")
        
        if assistant_response:
            whatsapp_service.send_whatsapp_message(
                phone_number=phone_number, 
                message=assistant_response
            )

    except (KeyError, IndexError):
        print("Received a non-message webhook or malformed data.")
        pass

    return {"status": "ok"}
    