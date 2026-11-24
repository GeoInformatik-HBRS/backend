import smtplib
import logging

import pytest

from src.use_cases.mail_sender import SendForwardMessageUseCase, ForwardingError
from src.models.attachment import Attachment

class FakeSMTP:
    """Replaces smtplib.SMTP for testing"""
    def __init__(self, error: Exception | None = None, fail_on_connect: bool = False) -> None:
        self.host = None
        self.port = None
        self.messages = []
        self._error = error
        self._fail_on_connect = fail_on_connect

    def __call__(self, host, port, timeout) -> "FakeSMTP":
        self.host = host
        self.port = port

        if self._fail_on_connect and self._error is not None:
            raise self._error
        return self

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False
    
    def send_message(self, msg):
        if self._error is not None and not self._fail_on_connect:
            raise self._error
        self.messages.append(msg)


def test_sends_message_with_attachments(monkeypatch) -> None:
    # arrange
    monkeypatch.setenv("SMTP_HOST", "smtp.localhost")
    monkeypatch.setenv("SMTP_PORT", "2525")
    monkeypatch.setenv("SMTP_FROM", "noreply@localhost")

    fake = FakeSMTP()
    photo1 = Attachment(filename="photo1.jpg", data=b"jpeg-data", content_type="image/jpeg")
    photo2 = Attachment(filename="photo2.png", data=b"png-data", content_type="image/png")
    attachments = [photo1, photo2]
    usecase = SendForwardMessageUseCase(fake)

    subject = "Neue Meldung: Straßenschäden"
    body = "Eine neue Meldung über einen Straßenschaden ist über das Meldeportal eingegangen."
    to = "to@localhost"

    # act
    usecase.execute(subject, body, to, attachments)

    # assert
    assert fake.host == "smtp.localhost"
    assert fake.port == 2525
    assert len(fake.messages) == 1

    msg = fake.messages[0]

    assert msg["Subject"] == subject
    assert msg.get_body().get_content() == body + "\n"
    assert msg["To"] == to
    assert msg["From"] == "noreply@localhost"

    att_list = list(msg.iter_attachments())
    assert len(att_list) == 2
    assert att_list[0].get_content_type() == "image/jpeg"
    assert att_list[0].get_filename() == "photo1.jpg"
    assert att_list[0].get_content() == b"jpeg-data"
    assert att_list[1].get_content_type() == "image/png"
    assert att_list[1].get_filename() == "photo2.png"
    assert att_list[1].get_content() == b"png-data"


@pytest.mark.parametrize("error, fail_on_connect", [(smtplib.SMTPException("rejected"), False), (OSError("refused"), True)])
def test_raises_error_on_failed_delivery(monkeypatch, error, fail_on_connect) -> None:
    # arrange
    monkeypatch.setenv("SMTP_HOST", "smtp.localhost")
    fake = FakeSMTP(error=error, fail_on_connect=fail_on_connect)
    usecase = SendForwardMessageUseCase(fake)

    subject = "Neue Meldung: Straßenschäden"
    body = "Eine neue Meldung über einen Straßenschaden ist über das Meldeportal eingegangen."
    to = "to@localhost"

    # act
    with pytest.raises(ForwardingError) as exc_info:
        usecase.execute(subject, body, to)

    # assert
    assert exc_info.value.__cause__ is error
    assert len(fake.messages) == 0


def test_only_logs_without_smtp_host(monkeypatch, caplog) -> None:
    # arrange
    monkeypatch.delenv("SMTP_HOST", raising=False)
    caplog.set_level(logging.INFO)

    fake = FakeSMTP()
    usecase = SendForwardMessageUseCase(fake)

    subject = "Neue Meldung: Straßenschäden"
    body = "Eine neue Meldung über einen Straßenschaden ist über das Meldeportal eingegangen."
    to = "to@localhost"

    # act
    usecase.execute(subject, body, to)

    # assert
    assert fake.host is None
    assert len(fake.messages) == 0
    assert "SMTP_HOST not set" in caplog.text
    assert subject in caplog.text
    assert to in caplog.text
