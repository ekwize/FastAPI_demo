import smtplib
from pathlib import Path

from PIL import Image
from pydantic import EmailStr

from src.config import settings
from src.tasks.celery import celery
from src.tasks.email_templates import create_booking_confirmation_template


@celery.task
def process_pic(
    path: str,
):
    im_path = Path(path)
    im = Image.open(im_path)
    im_resized = im.resize((1000, 500))
    im_resized = im.resize((200, 100))
    im_resized.save(f"src/static/images/resized_1000_500_{im_path.name}")
    im_resized.save(f"src/static/images/resized_200_100_{im_path.name}")

@celery.task  
def send_booking_confirmation_email(
    booking: dict,
    email_to: EmailStr,
):
    msg_content = create_booking_confirmation_template(booking, email_to)

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg_content)
    # logger.info(f"Successfully send email message to {email_to}")    