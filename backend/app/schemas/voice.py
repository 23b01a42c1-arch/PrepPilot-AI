from pydantic import BaseModel


class VoiceAnswerRequest(BaseModel):

    session_id: str

    audio_filename: str