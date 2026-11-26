from pydantic import BaseModel


class ReportRequest(BaseModel):
    """A citizen's defect report"""
    category: str
