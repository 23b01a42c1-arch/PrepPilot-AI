from fastapi import APIRouter, UploadFile, File
import shutil
import os

from app.services.parser import extract_text
from app.services.resume_analyzer import ResumeAnalyzer

router = APIRouter()

UPLOAD_FOLDER = "uploads"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...)
):

    file_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    with open(
        file_path,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    resume_text = extract_text(
        file_path
    )

    resume_data = (
        ResumeAnalyzer()
        .analyze_resume(
            resume_text
        )
    )

    return {
        "filename": file.filename,
        "resume_data": resume_data
    }