import smtplib
import json

from datetime import datetime

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def send_pdf_to_sn():
    """
    TODO
    """
    with open('/home/jakelamers/Documents/Code/python/send_daily_to_sn/config.json','r') as file:
        config = json.load(file)

    # Email configuration
    sender_email = config["sender_email"]
    receiver_email = config["receiver_email"]
    password = config["password"]

    # Create message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = f"{datetime.today().strftime('%Y-%m-%d')} Daily Journal"

    # Email body
    body = ""
    message.attach(MIMEText(body, "plain"))

    filename = f"{datetime.today().strftime('%Y-%m-%d')}.pdf"
    with open(filename, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename= {filename}")
    message.attach(part)

    # Send email
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, password)
            server.send_message(message)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")
