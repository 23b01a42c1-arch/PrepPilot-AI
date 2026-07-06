from pydantic import BaseModel


class FinishInterviewRequest(BaseModel):
    session_id: str