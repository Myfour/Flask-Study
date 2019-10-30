from flask_mail import Message
from flask import current_app


def send_email(to, subject, template, **kwargs):
    
