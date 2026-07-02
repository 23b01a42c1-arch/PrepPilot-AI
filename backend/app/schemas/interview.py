from pydantic import BaseModel


class GenerateInterviewRequest(BaseModel):

    resume_filename: str

    jd_text: str