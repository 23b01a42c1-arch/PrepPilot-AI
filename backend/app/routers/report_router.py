from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.core.session_store import session_manager
from app.services.report_generator_v2 import ReportGeneratorV2

router = APIRouter()


class ReportRequest(BaseModel):
    session_id: str


@router.post("/generate")
def generate_report(request: ReportRequest):

    session = session_manager.get_session(request.session_id)

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Interview session not found."
        )

    engine = session["engine"]

    history = engine.get_history()

    report = ReportGeneratorV2().generate(
        history=history,
        resume_data=session["resume_data"],
        jd_data=session["jd_data"]
    )

    return report