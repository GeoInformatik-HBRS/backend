from pydantic import BaseModel


class Attachment(BaseModel):
    """An email attachment (report photo)"""
    filename: str
    data: bytes
    content_type: str
