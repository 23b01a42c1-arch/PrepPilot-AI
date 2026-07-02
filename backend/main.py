from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.routers.resume_router import router as resume_router
from app.routers.interview_router import router as interview_router
from app.routers.voice_router import router as voice_router
from app.routers.report_router import router as report_router
from app.routers.upload_voice_router import router as upload_voice_router
from app.routers.auth_router import router as auth_router
app = FastAPI(
    title="AI Interview Assistant",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(
    resume_router,
    prefix="/resume",
    tags=["Resume"]
)

app.include_router(
    interview_router,
    prefix="/interview",
    tags=["Interview"]
)

app.include_router(
    voice_router,
    prefix="/voice",
    tags=["Voice"]
)

app.include_router(
    report_router,
    prefix="/report",
    tags=["Report"]
)

app.include_router(
    upload_voice_router,
    prefix="/voice",
    tags=["Voice Upload"]
)

app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"]
)

app.mount(
    "/audio",
    StaticFiles(directory="audio"),
    name="audio"
)

@app.get("/")
def home():
    return {
        "message": "AI Interview Assistant API Running"
    }
from app.database.db import Base, engine

Base.metadata.create_all(bind=engine)