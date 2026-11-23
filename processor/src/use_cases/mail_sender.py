import smtplib
import logging
import os

from email.message import EmailMessage

logger = logging.getLogger(__name__)

class ForwardingError(Exception):
    """Raised when a message could not be forwarded."""

class SendForwardMessageUseCase:
    def __init__(self, smtp=smtplib.SMTP) -> None:
        self._smtp=smtp
    
    def execute(self, subject: str, body: str, to: str, attachment=None) -> None:
        """Send E-Mail using EmailMessage and smtplib"""
        # get values from environmental varibles 
        smtphost = os.environ.get("SMTP_HOST")
        smtpport = int(os.environ.get("SMTP_PORT", 25))
        smtpfrom = os.environ.get("SMTP_FROM", "noreply@geoinfprojekt.de") # woher kommt "from"

        # log instead of send if no host specified
        if not smtphost:
            logger.info("Logging because no Host is configured. Recipient: %s, Subject: %s", to, subject)
            return

        # create email message
        msg = EmailMessage()
    
        msg['Subject'] = subject
        msg['To'] = to
        msg['From'] = smtpfrom
    
        msg.set_content(body)
        if attachment is not None:
            msg.add_attachment(attachment) #format des anhangs?

        # send mail, ForwardingError when failed
        try:
            with self._smtp(smtphost, smtpport, timeout=10) as smtp:
                smtp.send_message(msg)
        except (smtplib.SMTPException, OSError) as e:
            raise ForwardingError(f"Sending Mail to {to} failed.") from e
