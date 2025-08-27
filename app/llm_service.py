import os
import json
from openai import OpenAI
from openai.types.chat import ChatCompletionToolParam
from sqlalchemy.orm import Session
from . import services

# Initialize the client once
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# A mapping to easily call Python functions
available_tools = {
    "get_available_slots": services.get_available_slots,
    "book_appointment": services.book_appointment,
}

# The JSON definitions that send to the LLM
tools_definitions: list[ChatCompletionToolParam] = [
    {
        "type": "function",
        "function": {
            "name": "get_available_slots",
            "description": "Get a list of available appointment time slots for a specific service, staff member, and date.",
            "parameters": {
                "type": "object",
                "properties": {
                    "service_name": {"type": "string", "description": "The name of the service, e.g., 'Men''s Haircut'"},
                    "staff_name": {"type": "string", "description": "The name of the staff member, e.g., 'Sarah'"},
                    "date_str": {"type": "string", "description": "The desired date for the appointment, e.g., 'this Friday' or '2025-08-29'"},
                },
                "required": ["service_name", "staff_name", "date_str"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "book_appointment",
            "description": "Book an appointment for a customer.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_phone": {"type": "string", "description": "The customer's phone number."},
                    "service_name": {"type": "string", "description": "The name of the service to book."},
                    "staff_name": {"type": "string", "description": "The name of the staff member for the appointment."},
                    "appointment_time_str": {"type": "string", "description": "The specific time for the appointment, e.g., '3:00 PM'"},
                },
                "required": ["customer_phone", "service_name", "staff_name", "appointment_time_str"],
            },
        },
    },
]


def run_conversation(db: Session, conversation_history: list, user_message: str, customer_phone: str):
    """
    The main conversation orchestrator.
    """
    conversation_history.append({"role": "user", "content": user_message})

    # --- First API Call to the LLM ---
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=conversation_history,
        tools=tools_definitions,
        tool_choice="auto",
    )
    response_message = response.choices[0].message
    conversation_history.append(response_message)

    # --- Check if the LLM wants to call a tool ---
    if response_message.tool_calls:
        for tool_call in response_message.tool_calls:
            if tool_call.type == "function":
                function_name = tool_call.function.name
                function_to_call = available_tools[function_name]
                function_args = json.loads(tool_call.function.arguments)

                if function_name == "book_appointment":
                    function_args["customer_phone"] = customer_phone
                
                print(f"🤖 LLM wants to call tool: {function_name} with args: {function_args}")
                
                function_response = function_to_call(db=db, **function_args)
                
                print(f"🛠️ Tool responded with: {function_response}")

                conversation_history.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": str(function_response),
                    }
                )
        
        # Second API call with the tool's result
        final_response = client.chat.completions.create(
            model="gpt-4o",
            messages=conversation_history,
        )
        return final_response.choices[0].message.content

    # If no tool call, just return the text response
    else:
        return response_message.content