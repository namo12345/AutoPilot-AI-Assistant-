from agents.email_reader_agent import fetch_latest_emails

print("\U0001F50D Fetching your recent emails...\n")
emails = fetch_latest_emails(n=5)

for idx, email in enumerate(emails, 1):
    print(f"\n\U0001F4E9 Email {idx}:")
    print(f"From: {email['from']}")
    print(f"Subject: {email['subject']}")
    print(f"Snippet: {email['snippet']}")
    print(f"\u2705 Summary: {email['summary']}")
    if email['attachments']:
        print("\n📎 Attachment Summaries:")
        for fname, summary in email['attachments']:
            print(f"- {fname}: {summary}")
