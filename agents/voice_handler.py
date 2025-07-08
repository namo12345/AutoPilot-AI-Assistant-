import os
import logging
import speech_recognition as sr
from pydub import AudioSegment
from telegram import Update
from telegram.ext import ContextTypes
from dateutil import parser as date_parser

from agents.attachment_summarizer import summarize_attachment
from agents.email_summarizer import summarize_mail
from agents.reminder_agent import create_calendar_event
from utils.email_sender_agent import send_email_with_gpt
from utils.deep_research_agent import research_topic
from utils.nlu_agent import parse_intent_with_llm

logger = logging.getLogger(__name__)

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # 1. Download and convert voice to WAV
        voice_file = await context.bot.get_file(update.message.voice.file_id)
        file_path = "voice.oga"
        await voice_file.download_to_drive(file_path)

        wav_path = "voice.wav"
        AudioSegment.from_file(file_path).export(wav_path, format="wav")

        # 2. Transcribe with SpeechRecognition
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_path) as source:
            audio = recognizer.record(source)
        recognized_text = recognizer.recognize_google(audio)
        logger.info(f"🎤 Recognized voice: {recognized_text}")

        await update.message.reply_text(f"🤖 You said: \"{recognized_text}\"")

        # 3. Parse intent using LLM
        parsed = parse_intent_with_llm(recognized_text)
        logger.info(f"🧠 Parsed intent: {parsed}")

        intent = parsed.get("intent")

        if intent == "summarize_mails":
            await summarize_mail(update, context)

        elif intent == "summarize_attachments":
            await summarize_attachment(update, context)

        elif intent == "set_reminder":
            task = parsed.get("task")
            time_str = parsed.get("time")
            if task and time_str:
                try:
                    start_time = date_parser.parse(time_str, fuzzy=True)
                    await update.message.reply_text("⏰ Creating reminder...")
                    response = create_calendar_event(task, start_time)
                    await update.message.reply_text(response)
                except Exception as e:
                    logger.error(f"❌ Reminder creation error: {e}")
                    await update.message.reply_text("⚠️ Failed to parse time for reminder.")
            else:
                await update.message.reply_text("⚠️ Couldn’t extract both task and time.")

        elif intent == "send_email":
            email = parsed.get("email")
            message = parsed.get("message")
            if email and message:
                await update.message.reply_text("📧 Sending email...")
                result = send_email_with_gpt(email, message)
                await update.message.reply_text(result)
            else:
                await update.message.reply_text("⚠️ Missing email address or message.")

        elif intent in ["do_research", "research"]:
            topic = parsed.get("topic") or recognized_text
            await update.message.reply_text(f"🔍 Researching: {topic}...")
            summary = research_topic(topic)
            await update.message.reply_text(summary)

        elif intent == "get_weather":
            await update.message.reply_text("🌤️ Weather functionality coming soon.")

        else:
            await update.message.reply_text(f"🤖 Sorry, I didn’t understand intent: '{intent}'")

        # Clean up
        os.remove(file_path)
        os.remove(wav_path)

    except Exception as e:
        logger.error(f"❌ Voice handler error: {str(e)}")
        await update.message.reply_text("⚠️ Failed to process your voice message. Try again slowly.")
