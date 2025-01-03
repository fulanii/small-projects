import os
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage

from celery import Celery
from celery.schedules import crontab

load_dotenv()  

app = Celery("send_email",broker='redis://localhost:6379/0')
app.conf.broker_connection_retry_on_startup = True

app.conf.beat_schedule = {
    'send-daily-email': {
        'task': "celery_app.send_email",
        'schedule': crontab(minute="*"),# execute every minute
        'args': []  # No arguments since send_email() doesn't accept args
    }
    }

@app.task
def send_email():
    print("Task started: Sending email...")
    try:
        msg = EmailMessage()
        msg.set_content("This is a test email sent from Celery and Redis")
        msg['Subject'] = "celery and redis test" 
        msg['From'] = os.getenv("FROM_EMAIL")
        msg['To'] = os.getenv("TO_EMAIL")

        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login(os.getenv("FROM_EMAIL"), os.getenv("EMAIL_PASS"))
            smtp.send_message(msg)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")
