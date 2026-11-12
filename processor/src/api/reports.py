import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.use_cases.category_routing import CategoryRoutingUseCase

router = APIRouter()
logger = logging.getLogger(__name__)
usecase = CategoryRoutingUseCase()

class ReportRequest(BaseModel):
    category: str

@router.post("/reports", status_code=204)
def reports(request: ReportRequest) -> None:
    """Route a report's category internally; respond 204, 400 (unknown) or 422 (invalid)."""
    try:
        # use CategoryRoutingUseCase to get department
        department = usecase.execute(request.category)
    except ValueError:
        # raise 400 exception
        logger.warning("Rejected report: unsupported category=%r", request.category)
        raise HTTPException(status_code=400, detail="Unsupported category")
    logger.info("Report routed: category=%s department=%s", request.category, department)
