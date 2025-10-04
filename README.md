# Salon WhatsApp AI Booking Bot 🤖

This project is a sophisticated, AI-powered chatbot designed to automate appointment bookings for a salon via WhatsApp. It uses natural language processing to understand customer requests, checks for availability, and saves confirmed bookings to a database.

The entire system is built with a modern Python backend and integrates directly with the Meta WhatsApp Cloud API and the OpenAI API for its intelligence.

---
## ✨ Features

* **Conversational Booking:** Customers can book, and eventually modify or cancel, appointments using natural language.
* **AI-Powered:** Utilizes OpenAI's `gpt-4o` for state-of-the-art understanding, conversation, and tool use.
* **Database Integration:** All customers, staff, services, and bookings are stored and managed in a PostgreSQL database.
* **WhatsApp Integration:** Connects directly to the Meta WhatsApp Cloud API for sending and receiving messages.
* **Tool Use / Function Calling:** The AI can intelligently decide when to call backend functions to check for availability or confirm a booking.

---
## 🛠️ Technology Stack

* **Backend:** FastAPI
* **AI:** OpenAI API (gpt-4o)
* **Database:** PostgreSQL with SQLAlchemy ORM
* **Messaging:** Meta WhatsApp Cloud API
* **Language:** Python 3.9+

---
## 🚀 Setup and Installation

Follow these steps to get the project running on your local machine for development.

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd salon-bot
```

### 2. Create and Activate a Virtual Environment
It's highly recommended to use a virtual environment.

```bash
# Create the virtual environment
python -m venv .venv

# Activate it
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up PostgreSQL Database
You need a running PostgreSQL instance.
* Install PostgreSQL for your operating system.
* Start the PostgreSQL service.
* Open the psql shell and create a dedicated user and database for the project.
```bash
-- Replace 'myuser' and 'mypassword' with your own credentials
CREATE USER myuser WITH PASSWORD 'mypassword';
CREATE DATABASE salon OWNER myuser;
GRANT ALL PRIVILEGES ON DATABASE salon TO myuser;
```

### 5. Create Database Tables
Run the script to create the tables defined in the SQLAlchemy models.
```bash
python create_tables.py
```

## ⚙️ Configuration
The application requires several API keys and secrets.
* Create the .env file: In the root directory, create a file named .env.
* Add your credentials: Copy the structure below into your .env file and fill in your actual values.
```bash
# .env file template

# PostgreSQL Database Connection URL
# Format: postgresql://<user>:<password>@<host>:<port>/<dbname>
DATABASE_URL="postgresql://myuser:mypassword@localhost/salon"

# OpenAI API Key
OPENAI_API_KEY="sk-..."

# Meta WhatsApp API Credentials
# Get these from your App Dashboard -> WhatsApp -> API Setup
META_ACCESS_TOKEN="your_permanent_meta_access_token"
PHONE_NUMBER_ID="your_whatsapp_phone_number_id"

# A secret string you create yourself for webhook verification
META_VERIFY_TOKEN="your_unique_and_secret_verify_token"
```

## ▶️ Running the Application
You'll need two terminals running simultaneously for local development.

Terminal 1: Start the Backend Server - This runs the main FastAPI application.
```bash
uvicorn app.main:app --reload
```

The server will be running on http://127.0.0.1:8000.

Terminal 2: Start the ngrok Tunnel

This exposes your local server to the internet so Meta's webhooks can reach it.

```bash
ngrok http 8000
```

Copy the HTTPS forwarding URL provided by ngrok (e.g., https://<random-string>.ngrok-free.app).

Final Step: Configure the Webhook

* Go to your Meta App Dashboard -> WhatsApp -> Configuration.

* Click "Edit" on the Webhooks section.

* Paste your ngrok HTTPS URL, adding /webhook at the end.

* Paste your META_VERIFY_TOKEN from your .env file into the "Verify Token" field.

* Verify and save, then subscribe to the messages event.

## ✅ Testing

* Send a message from your verified personal WhatsApp number to the test number provided by Meta.
* You should see the bot respond in your WhatsApp chat.
* Check your Uvicorn terminal for detailed logs of the conversation, including AI tool calls.
* After a successful booking, you can verify the data was saved in your database:

```bash
# Connect to the database
psql -U myuser -d salon -W

# Check the bookings table
SELECT * FROM bookings;
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📞 Support

If you have any questions or need help setting up the project, please open an issue or contact the maintainer.

