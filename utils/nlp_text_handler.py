# utils/nlp_text_handler.py

from telegram import Update
from telegram.ext import ContextTypes
from utils.nlu_agent import parse_intent_with_llm
from agents.email_summarizer import summarize_mail
from agents.attachment_summarizer import summarize_attachment
from utils.deep_research_agent import research_topic
from utils.email_sender_agent import send_email_with_gpt
from agents.reminder_agent import create_calendar_event

async def handle_nlp_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.message.text
        await update.message.reply_text(f"🤖 You typed: \"{text}\"")

        parsed = parse_intent_with_llm(text)
        intent = parsed.get("intent")

        if intent == "summarize_mails":
            await summarize_mail(update, context)

        elif intent == "summarize_attachments":
            await summarize_attachment(update, context)

        elif intent == "set_reminder":
            task = parsed.get("task")
            time = parsed.get("time")
            if task and time:
                try:
                    response = create_calendar_event(task, time)
                    await update.message.reply_text(response)
                except Exception as e:
                    await update.message.reply_text(f"⚠️ Error creating reminder: {str(e)}")
            else:
                await update.message.reply_text("⚠️ Couldn’t extract task or time.")

        elif intent == "send_email":
            email = parsed.get("email")
            message = parsed.get("message")
            if email and message:
                result = send_email_with_gpt(email, message)
                await update.message.reply_text(result)
            else:
                await update.message.reply_text("⚠️ Missing email or message.")

        elif intent in ["do_research", "research"]:
            topic = parsed.get("topic") or text
            summary = research_topic(topic)
            await update.message.reply_text(summary)

        elif intent == "get_weather":
            await update.message.reply_text("🌤️ Weather support coming soon!")

        else:
            await update.message.reply_text(f"🤖 Sorry, I didn’t understand your intent: {intent}")

    except Exception as e:
        await update.message.reply_text("⚠️ Failed to process your message. Try again slowly.")
