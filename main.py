import flask
import functions_framework
import os
import smtplib
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
from email.message import EmailMessage
from flask import make_response, jsonify


@functions_framework.http
def send_email(request) -> flask.typing.ResponseReturnValue:
    load_dotenv(find_dotenv(filename=".env", raise_error_if_not_found=True), verbose=True)
    smtp_server = os.getenv("SMTP_SERVER")
    receiver_email = os.getenv("RECEIVER")
    sender_email = os.getenv("SENDER")
    password = os.getenv("PASSWORD")

    msg = EmailMessage()
    msg["Subject"] = f"Checking mail account: {datetime.date(datetime.now())}"
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg.set_content("email for checking account's accessibility")
    try:
        with smtplib.SMTP_SSL(smtp_server, 465) as smtp_server:
            smtp_server.login(sender_email, password)
            smtp_server.send_message(msg)
    except Exception as e:
        response = {
            "status": "error",
            "message": str(e)
        }
        return make_response(jsonify(response), 500)
    else:
        response = {
            "status": "success",
            "message": "Email sent successfully."
        }
        return make_response(jsonify(response), 200)
