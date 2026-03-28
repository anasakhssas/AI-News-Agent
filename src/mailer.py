import os
import smtplib
from email.message import EmailMessage
from typing import List, Dict
from datetime import datetime

def send_newsletter(summary: str, articles: List[Dict[str, str]]):
    """Sends the formatted email to the user."""
    sender_email = os.getenv("EMAIL_USER")
    sender_password = os.getenv("EMAIL_PASS")
    receiver_email = os.getenv("EMAIL_TO")

    if not all([sender_email, sender_password, receiver_email]):
        raise ValueError("Email credentials are missing in environment variables.")

    msg = EmailMessage()
    
    today_str = datetime.now().strftime("%A, %B %d, %Y")
    msg['Subject'] = f"☕ Daily Intelligence Briefing - {today_str}"
    msg['From'] = sender_email
    msg['To'] = receiver_email

    text_content = f"Good morning!\n\nHere is your daily briefing:\n\n{summary}\n\nTop Stories:\n"
    for a in articles:
        text_content += f"- {a['title']}\n  {a['url']}\n"
    
    html_links = "".join([f"<li style='margin-bottom: 10px;'><a href='{a['url']}' style='color: #007bff; text-decoration: none;'><strong>{a['title']}</strong></a> <span style='color: #6c757d; font-size: 0.9em;'>({a['source']})</span></li>" for a in articles])
    html_content = f"""
    <html>
        <body style="font-family: Arial, sans-serif; color: #333; line-height: 1.6; max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #2c3e50;">Good morning! ☕</h2>
            <div style="background-color: #f8f9fa; padding: 15px; border-left: 4px solid #007bff; margin-bottom: 25px;">
                <p style="margin: 0; font-size: 16px;">{summary}</p>
            </div>
            <h3 style="color: #2c3e50; border-bottom: 2px solid #eee; padding-bottom: 5px;">Today's Global Intel</h3>
            <ul style="list-style-type: none; padding-left: 0;">
                {html_links}
            </ul>
            <p style="font-size: 12px; color: #888; margin-top: 30px; border-top: 1px solid #eee; padding-top: 10px; text-align: center;">
                Generated automatically by your Groq AI Agent via GitHub Actions.
            </p>
        </body>
    </html>
    """

    msg.set_content(text_content)
    msg.add_alternative(html_content, subtype='html')

    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "465"))

    try:
        with smtplib.SMTP_SSL(smtp_host, smtp_port) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
        print("Email sent successfully!")
        return True
    except smtplib.SMTPAuthenticationError as e:
        raise RuntimeError(
            "SMTP authentication failed. For Gmail, use a Google App Password (not your normal account password)."
        ) from e
    except Exception as e:
        raise RuntimeError(f"Error sending email: {e}") from e
