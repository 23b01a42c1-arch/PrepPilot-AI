from deepgram import (
    DeepgramClient,
    PrerecordedOptions,
    FileSource
)

import os
from dotenv import load_dotenv

load_dotenv()


class SpeechToText:

    def __init__(self):

        self.client = DeepgramClient(
            os.getenv("DEEPGRAM_API_KEY")
        )

    def transcribe(
        self,
        audio_path
    ):

        with open(
            audio_path,
            "rb"
        ) as file:

            payload: FileSource = {
                "buffer": file.read()
            }

        options = (
            PrerecordedOptions(
                model="nova-2",
                language="en-IN",
                smart_format=True,
                punctuate=True,
                paragraphs=True,
                filler_words=False,
                diarize=False
            )
        )

        response = (
            self.client.listen.rest.v("1")
            .transcribe_file(
                payload,
                options
            )
        )

        transcript = (
            response.results.channels[0]
            .alternatives[0]
            .transcript
        )

        return {
            "text": transcript
        }