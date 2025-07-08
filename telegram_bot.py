import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, filters
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from agents.voice_handler import handle_voice
from agents.attachment_summarizer import summarize_attachment
from agents.email_summarizer import summarize_mail
from utils.email_sender_agent import send_email_with_gpt
from utils.deep_research_agent import research_topic
from agents.reminder_agent import create_calendar_event
from utils.nlp_text_handler import handle_nlp_text  # NEW: for NLP text inputs

# Load environment variables
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
USER_ID = int(os.getenv("TELEGRAM_USER_ID"))

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Scheduler for future tasks
scheduler = AsyncIOScheduler()

# --- Command Handlers ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_msg = (
        "👋 Welcome to Autopilot AI Bot!\n\n"
        "Here’s what I can do:\n"
        "📎 /summary – Summarize attached documents\n"
        "📬 /mailsummary – Summarize recent Gmail inbox\n"
        "✉️ /sendmail <to> | <subject> | <body> – Send an email\n"
        "🔍 /topic <your topic> – Deep research a topic\n"
        "⏰ /remind <date> | <time> | <text> – Set a Google Calendar reminder\n"
        "🎙️ Voice commands:\n"
        "     'summarize my mail', 'research quantum computing', or 'remind me tomorrow at 10am'\n"
        "💬 Text me like a human:\n"
        "     'send email to xyz@gmail.com that I miss you' or 'set reminder to drink water at 6pm'"
    )
    await update.message.reply_text(welcome_msg)

async def summarize_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await summarize_attachment(update, context)

async def mail_summary_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await summarize_mail(update, context)

async def sendmail_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args = update.message.text.split(" ", 1)[1]
        to, subject, body = map(str.strip, args.split("|"))
        response = send_email_with_gpt(to, body)
        await update.message.reply_text(response)
    except Exception as e:
        logger.error(f"Sendmail error: {e}")
        await update.message.reply_text("⚠️ Error sending email. Format: /sendmail to | subject | body")

async def research_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        query = " ".join(context.args)
        if not query:
            await update.message.reply_text("❌ Please provide a topic after /topic")
            return
        await update.message.reply_text("🔍 Researching topic...")
        summary = research_topic(query)
        await update.message.reply_text(summary)
    except Exception as e:
        logger.error(f"Research error: {e}")
        await update.message.reply_text(f"❌ Error: {e}")

async def remind_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args = update.message.text.split(" ", 1)[1]
        date, time, *text_parts = args.split("|")
        text = "|".join(text_parts).strip()
        response = create_calendar_event(date.strip(), time.strip(), text)
        await update.message.reply_text(response)
    except Exception as e:
        logger.error(f"Reminder error: {e}")
        await update.message.reply_text("⚠️ Error creating reminder. Format: /remind date | time | text")

# --- Main Entry Point ---

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("summary", summarize_command))
    app.add_handler(CommandHandler("mailsummary", mail_summary_command))
    app.add_handler(CommandHandler("sendmail", sendmail_command))
    app.add_handler(CommandHandler("topic", research_command))
    app.add_handler(CommandHandler("remind", remind_command))

    # Message handlers
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))  # 🎙️ Voice
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_nlp_text))  # 💬 Text

    scheduler.start()
    logger.info("🚀 Telegram bot is running...")

    app.run_polling()
