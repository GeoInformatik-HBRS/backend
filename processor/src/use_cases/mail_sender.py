import smtplib
import logging
import os

from email.message import EmailMessage

logger = logging.getLogger(__name__)


class ForwardingError(Exception):
    """Raised when a message could not be forwarded."""


def send_forward_message(subject, body, to, attachment=None) -> None:
    """Send E-Mail using EmailMessage and smtplib"""
    # get values from environtmental varibles 
    host = os.environ.get("SMTP_HOST")
    port = int(os.environ.get("SMTP_PORT", 25))

    # create email message object to build the message in
    msg = EmailMessage()

    msg['Subject'] = subject
    msg['To'] = to

    msg.set_content(body)
    # TODO: attachments?

    # log instead of send if no host specified, TODO: move up?
    if not host:
        logger.info("Logging because no Host is configured. Recipient: %s, Subject: %s", to, subject)
        return

    # send mail, ForwardingError when failed
    try:
        with smtplib.SMTP(host, port) as smtp:
            smtp.send_message(msg)
    except (smtplib.SMTPException, OSError) as e:
        raise ForwardingError(f"Sending Mail to {to} failed.") from e
