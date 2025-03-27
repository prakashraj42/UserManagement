from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import BaseModel, EmailStr
from dotenv import load_dotenv
import os
from jinja2 import Template
from pathlib import Path
import asyncio  
import random

def generate_otp():
    return str(random.randint(100000, 999999))

load_dotenv()

TEMPLATE_FOLDER = Path(__file__).parent / "Templates"

MAIL_USERNAME = os.getenv("EMAIL_USERNAME")
MAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
MAIL_FROM = os.getenv("MAIL_FROM")

if not MAIL_USERNAME or not MAIL_PASSWORD or not MAIL_FROM:
    raise ValueError(" missing env variyabels")

conf = ConnectionConfig(
    MAIL_USERNAME = MAIL_USERNAME,
    MAIL_PASSWORD= MAIL_PASSWORD,
    MAIL_FROM = MAIL_FROM,
    MAIL_PORT= 587,
    MAIL_SERVER= "smtp.gmail.com",
    MAIL_STARTTLS= True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    TEMPLATE_FOLDER=TEMPLATE_FOLDER
    )

class Emailshema(BaseModel):
    email: EmailStr
    subject : str
    body : str

def send_org_reg_mail(email: EmailStr, org_name: str):

    template_path = TEMPLATE_FOLDER / "otp_send.html"

    if not template_path.exists():
        raise FileNotFoundError(f"template file not found: {template_path}")
    
    with open(template_path, "r", encoding="utf-8") as file:
        template = Template(file.read())

    html_content = template.render(email=email, org_name=org_name)

    message = MessageSchema(
        subject=" welcome to our portal",
        recipients=[email],
        body=html_content,
        subtype="html"
    )

    fm =FastMail(conf)
    asyncio.run(fm.send_message(message))

    