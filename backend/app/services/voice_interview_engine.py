from app.services.speech_to_text import (
    SpeechToText
)

from app.services.text_to_speech import (
    TextToSpeech
)


class VoiceInterviewEngine:

    def __init__(self):

        self.stt = SpeechToText()

        self.tts = TextToSpeech()

    # -----------------------------
    # Submit Audio
    # -----------------------------

    def submit_audio(
        self,
        session,
        audio_path
    ):

        transcript = (
            self.stt.transcribe(
                audio_path
            )
        )

        answer = transcript["text"]

        engine = session["engine"]

        result = (
            engine.submit_answer(
                answer
            )
        )
        result = engine.submit_answer(answer)

        print("\n====================")
        print("TRANSCRIPT:")
        print(answer)

        print("\nRESULT:")
        print(result)
        print("====================")

        if result["type"] != "completed":

            self.tts.speak(
                result["question"],
                "audio/question.mp3"
            )

            result["audio"] = "/audio/question.mp3"

        result["transcript"] = answer

        return result

    # -----------------------------
    # History
    # -----------------------------

    def get_history(
        self,
        session
    ):

        return (
            session["engine"]
            .get_history()
        )