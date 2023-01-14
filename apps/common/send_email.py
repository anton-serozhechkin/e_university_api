from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from settings import Settings


conf = ConnectionConfig(
    MAIL_USERNAME=Settings.MAIL_USERNAME,
    MAIL_PASSWORD=Settings.MAIL_PASSWORD,
    MAIL_FROM=Settings.MAIL_FROM,
    MAIL_PORT=Settings.MAIL_PORT,
    MAIL_SERVER=Settings.MAIL_SERVER,
    MAIL_FROM_NAME=Settings.MAIL_FROM_NAME,
    MAIL_STARTTLS=Settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=Settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=Settings.USE_CREDENTIALS,
    TEMPLATE_FOLDER=Settings.TEMPLATE_FOLDER,
)


async def send_email_async(subject: str, email_to: str, body: str):
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        body=body,
        subtype='html',
    )

    fm = FastMail(conf)
    await fm.send_message(message, template_name='email.html')