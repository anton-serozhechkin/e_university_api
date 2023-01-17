import abc

from fastapi_mail import ConnectionConfig, FastMail

from apps.common.exceptions import (
    ApiError,
    ConnectionErrors,
    DBProvaiderError,
    PydanticClassRequired,
    TemplateFolderDoesNotExist,
    WrongFile,
)
from apps.common.schemas import MessageSchema
from settings import Settings


class EmailManagerInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass) -> bool:
        return hasattr(subclass, "send_email") and callable(subclass.send_email)

    @abc.abstractmethod
    def send_email_async(
        self,
        message: MessageSchema,
        template_name: str,
    ) -> None:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def configuration(self) -> ConnectionConfig:
        raise NotImplementedError


class EmailManager(EmailManagerInterface):
    @property
    def configuration(self) -> ConnectionConfig:
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

    async def send_email_async(
        self,
        message: MessageSchema,
        template_name: str,
    ) -> None:
        fm = FastMail(self.configuration)
        try:
            await fm.send_message(message, template_name=template_name)
        except (
            ConnectionErrors,
            WrongFile,
            PydanticClassRequired,
            TemplateFolderDoesNotExist,
            ApiError,
            DBProvaiderError,
        ):
            # create message with smtp server access problems
            print("There is a problem with smtp server access")
            pass


email_manager = EmailManager()
