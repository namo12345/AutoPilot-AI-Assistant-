# utils/intent_parser.py

def parse_intent(text):
    text = text.lower()

    if "summary" in text or "summarize" in text:
        return "summary"

    if "send mail" in text or "email" in text:
        return "sendmail"

    if "remind me" in text or "reminder" in text:
        return "reminder"

    if "research" in text or "tell me about" in text or "what is":
        return "deepresearch"

    if "weather" in text:
        return "weather"

    if "holiday" in text or "off tomorrow" in text:
        return "holiday"

    return "unknown"
