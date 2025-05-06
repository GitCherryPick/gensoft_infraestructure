import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()

def send_email(to, subject, body):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = os.getenv('EMAIL_FROM')
    msg['To'] = to
    msg.set_content(body)

    print(f"Sending email... {os.getenv('EMAIL_FROM')}")
    try:
        with smtplib.SMTP(os.getenv("EMAIL_HOST"), 587) as smtp:
            smtp.starttls()
            smtp.login(os.getenv('EMAIL_USERNAME'), os.getenv('EMAIL_PASSWORD'))
            smtp.send_message(msg)
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")