import abc

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from settings import Settings
from typing import List


class EmailManagerInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass) -> bool:
        return (
            hasattr(subclass, "send_email")
            and callable(subclass.send_email)
        )

    @abc.abstractmethod
    def send_email_async(
        self,
        subject: str,
        email_to: List[str],
        attachments: str,
        body: dict,
        template_name: str,
        subtype: str,
    ) -> None:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def configuration(self) -> ConnectionConfig:
        raise NotImplementedError


class EmailManager(EmailManagerInterface):
    @property
    def configuration(self):
        return ConnectionConfig(
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

    def send_email_async(
        self,
        subject: str,
        email_to: List[str],
        attachments: str,
        body: dict,
        template_name: str,
        subtype: str,
    ) -> None:
        message = MessageSchema(
            subject=subject,
            recipients=email_to,
            attachments=attachments,
            template_body=body,
            subtype=subtype,
        )

        fm = FastMail(self.configuration)
        try:
            await fm.send_message(message, template_name=template_name)
        except Exception:
            # create message with smtp server access problems
            print("There is a problem with smtp server access")
            pass


email_manager = EmailManager()
