# 🤖 AutoPilot-AI-Assistant

**AutoPilot-AI-Assistant** is a powerful, AI-powered voice and text-based Telegram bot that automates everyday tasks like:
- 📧 Sending emails
- 📬 Summarizing Gmail inbox
- 📎 Summarizing document attachments
- 🔔 Creating reminders in Google Calendar
- 🔍 Doing deep research from web using LLMs
- 🗣️ Voice-based command interpretation
- 🧠 Natural Language Understanding using LLMs

---

## 🚀 Features

| Feature               | Description                                               |
|-----------------------|-----------------------------------------------------------|
| 📬 Mail Summary       | Summarizes latest emails from your Gmail inbox            |
| ✉️ Send Email         | Composes polished emails via voice/text                   |
| 📎 Attachment Summary | Summarizes uploaded PDFs or DOCs                          |
| 🔔 Reminders          | Creates Google Calendar events from casual text           |
| 🧠 Deep Research      | Web-scrapes and summarizes info on any topic              |
| 🎙️ Voice Commands     | Recognizes speech and parses into actionable intents       |
| 📩 NLP Text Commands  | You can also just type the same instructions              |

---

## 🛠 How It Works

- Telegram bot receives a voice/text message  
- Audio is converted to text (if needed)  
- Intent is parsed using LLM (`mistralai/mistral-7b-instruct` via OpenRouter)  
- Matching agent (email, reminder, research, etc.) is triggered  
- Result is sent back to the user via Telegram  

---

## 🤖 Agents Used

- `voice_handler` → Transcribes & parses voice commands  
- `nlp_text_handler` → Handles free-form text input  
- `email_sender_agent` → Sends Gmail via OAuth  
- `email_summarizer` → Fetches + summarizes last emails  
- `attachment_summarizer` → Summarizes attached documents  
- `reminder_agent` → Adds events to your Google Calendar  
- `deep_research_agent` → Scrapes web & summarizes content  
- `nlu_agent` → Converts natural language into structured JSON  

---

## ⚙️ .env File Setup

You must create a `.env` file in the root of your project:

```env
# OPENROUTER or OPENAI KEY
LLM_API_KEY=sk-or-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
LLM_MODEL=mistralai/mistral-7b-instruct

# TAVILY API (for deep research)
TAVILY_API_KEY=tvly-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# GMAIL OAuth2 Details
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REFRESH_TOKEN=your-refresh-token
GMAIL_USER=your-gmail@gmail.com

# CALENDAR OAuth2 Details
CALENDAR_CLIENT_ID=your-calendar-client-id.apps.googleusercontent.com
CALENDAR_CLIENT_SECRET=your-calendar-client-secret
CALENDAR_REFRESH_TOKEN=your-calendar-refresh-token

# TELEGRAM BOT
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
TELEGRAM_USER_ID=your-telegram-user-id (numeric)
````

---

## 🔑 Generate OAuth Tokens for Gmail/Calendar

Use our token generation helper script:

### ▶️ `generate_token.py` Script

```bash
python generate_token.py
```

### Step-by-Step

1. Go to [https://console.cloud.google.com](https://console.cloud.google.com)

2. Create a project and enable these APIs:

   * Gmail API
   * Google Calendar API

3. Under **APIs & Services > Credentials**:

   * Create OAuth credentials → Application type: Desktop
   * Note down Client ID and Client Secret

4. Run the script and paste:

   * Your Client ID
   * Client Secret
   * Scopes (comma-separated):

```bash
https://www.googleapis.com/auth/gmail.send,
https://www.googleapis.com/auth/gmail.readonly,
https://www.googleapis.com/auth/calendar
```

5. Copy the authorization URL into a browser → Authorize → Paste the returned code.

6. The script prints the refresh token to add in your `.env`.

---

## 💬 Example Commands

**Voice or Text (Free-form):**

```
summarize my email
send email to john@example.com saying I’ll be late
remind me tomorrow 8am to go jogging
do deep research on quantum teleportation
```

**Command Based (/slash):**

```
/mailsummary
/summary
/sendmail email@example.com | Subject | Body
/remind 2025-07-08 | 8:00 PM | Team Meeting
/topic AI for climate change
```

---

## 📦 Requirements

* Python 3.10+
* `requirements.txt` provided (install with `pip install -r requirements.txt`)
* Google API Credentials
* Telegram Bot Token
* OpenRouter API Key
* Tavily API Key (optional for deep research)

---

## 📌 Deployment Notes

This version is **single-user only** (linked to your own Gmail & Calendar).
To support multi-user authentication (for public deployment), you'd need:

* OAuth Consent Screen (Production)
* Per-user auth + token storage
* Backend server for user sessions

---

## 📂 Folder Structure

```
autopilot-ai-assistant/
├── agents/
│   ├── voice_handler.py
│   ├── email_summarizer.py
│   ├── reminder_agent.py
│   ├── attachment_summarizer.py
├── utils/
│   ├── llm_util.py
│   ├── email_sender_agent.py
│   ├── deep_research_agent.py
│   ├── nlu_agent.py
│   ├── nlp_text_handler.py
│   ├── generate_token.py
├── telegram_bot.py
├── .env
├── requirements.txt
└── README.md
```

---

## 🧠 Future Ideas

* Add Weather and News agents
* Multi-user support with login
* Dashboard to view reminders/emails
* File upload from voice

---

## 🙌 Built With

* 🧠 OpenRouter.ai (Mistral LLM)
* 🗂️ Tavily API for search
* 🎙️ SpeechRecognition + Pydub
* 📬 Gmail + Calendar API
* 🤖 python-telegram-bot
* ⏰ APScheduler

---

> ✨ Crafted by \[venkateshwara reddy] — for productivity with AI 🧠
