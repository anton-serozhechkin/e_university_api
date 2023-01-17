from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from settings import Settings
from typing import List


conf = ConnectionConfig(
    MAIL_USERNAME=Settings.MAIL_USERNAME,
    MAIL_PASSWORD=Settings.MAIL_PASSWORD,
    MAIL_FROM=Settings.MAIL_FROM,
    MAIL_PORT=Settings.MAIL_PORT,
    MAIL_SERVER=Settings.MAIL_SERVER,
    MAIL_FROM_NAME=Settings.MAIL_FROM_NAME,
    MAIL_TLS=Settings.MAIL_TLS,
    MAIL_SSL=Settings.MAIL_SSL,
    USE_CREDENTIALS=Settings.USE_CREDENTIALS,
    TEMPLATE_FOLDER=Settings.TEMPLATE_FOLDER,
)


async def send_email_async(
        subject: str,
        email_to: List[str],
        body: dict,
        template_name: str = 'email.html',
) -> None:
    message = MessageSchema(
        subject=subject,
        recipients=email_to,
        template_body=body,
        subtype="html",
    )

    fm = FastMail(conf)
    try:
        await fm.send_message(message, template_name=template_name)
    except Exception:
        # create message with smtp server access problems
        print("There is a problem with smtp server access")
        pass

