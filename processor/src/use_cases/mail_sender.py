import smtplib
import logging
import os

from email.message import EmailMessage
from src.models.attachment import Attachment

logger = logging.getLogger(__name__)

class ForwardingError(Exception):
    """Raised when a message could not be forwarded."""

class SendForwardMessageUseCase:
    def __init__(self, smtp_class=smtplib.SMTP) -> None:
        self._smtp_class = smtp_class
    
    def execute(self, subject: str, body: str, to: str, attachments: list[Attachment] | None = None) -> None:
        """Send E-Mail using EmailMessage and smtplib.
        
        Only logging when SMTP_HOST is not set.
        Needs SMTP_HOST, SMTP_PORT and SMTP_FROM from the environment.
        Raises ForwardingError when sending fails.
        """
        # get values from environment variables
        smtp_host = os.environ.get("SMTP_HOST")
        smtp_port = int(os.environ.get("SMTP_PORT", 25))
        smtp_from = os.environ.get("SMTP_FROM", "noreply@localhost")

        # log instead of send if no host specified
        if not smtp_host:
            logger.info("SMTP_HOST not set. Logging message: Recipient: %s, Subject: %s", to, subject)
            return

        # create email message
        msg = EmailMessage()
    
        msg['Subject'] = subject
        msg['To'] = to
        msg['From'] = smtp_from
    
        msg.set_content(body)

        # add attachments (pydantic model(filename, data, content_type))
        if attachments:
            for attachment in attachments:
                maintype, subtype = attachment.content_type.split("/")
                msg.add_attachment(attachment.data, maintype=maintype, subtype=subtype, filename=attachment.filename)

        # send mail, ForwardingError when failed
        try:
            with self._smtp_class(smtp_host, smtp_port, timeout=10) as smtp:
                smtp.send_message(msg)
        except (smtplib.SMTPException, OSError) as e:
            raise ForwardingError(f"Sending Mail to {to} failed.") from e
