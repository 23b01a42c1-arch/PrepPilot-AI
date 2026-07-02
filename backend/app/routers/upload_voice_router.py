from fastapi import APIRouter, UploadFile, File
import shutil
import os

router = APIRouter()

UPLOAD_DIR = "audio"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)


@router.post("/upload")
async def upload_audio(
    file: UploadFile = File(...)
):

    filepath = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    with open(
        filepath,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    return {
    "filename": file.filename,
    "path": filepath,
    "url": f"/audio/{file.filename}"
    }