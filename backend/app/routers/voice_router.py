from fastapi import APIRouter

from app.schemas.voice import (
    VoiceAnswerRequest
)

from app.core.session_store import (
    session_manager
)

from app.services.voice_interview_engine import (
    VoiceInterviewEngine
)

router = APIRouter()

voice_engine = VoiceInterviewEngine()


@router.post("/answer")
def answer_question(
    request: VoiceAnswerRequest
):

    session = session_manager.get_session(
        request.session_id
    )

    if session is None:

        return {

            "error": "Invalid session."
        }

    return voice_engine.submit_audio(

        session,

        request.audio_filename
    )