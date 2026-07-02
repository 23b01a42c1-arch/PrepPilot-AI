import asyncio
import os

import edge_tts


class TextToSpeech:

    def __init__(self):

        self.voice = "en-IN-NeerjaNeural"

    async def _generate(
        self,
        text,
        output_file
    ):

        communicate = edge_tts.Communicate(
            text=text,
            voice=self.voice
        )

        await communicate.save(output_file)

    def speak(
        self,
        text,
        output_file="audio/question.mp3"
    ):

        os.makedirs(
            os.path.dirname(output_file),
            exist_ok=True
        )

        asyncio.run(
            self._generate(
                text,
                output_file
            )
        )

        return output_file