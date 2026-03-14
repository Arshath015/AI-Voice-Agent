import asyncio
import edge_tts
from faster_whisper import WhisperModel
import uuid
import os


class WhisperSTT:
    def __init__(self):
        # small model is fast for CPU
        self.model = WhisperModel("small", compute_type="int8")

    def transcribe(self, audio_path: str) -> str:
        segments, _ = self.model.transcribe(audio_path)
        text = ""
        for segment in segments:
            text += segment.text + " "
        return text.strip()


class EdgeTTS:
    def __init__(self):
        self.voice = "en-US-JennyNeural"

    async def generate(self, text: str) -> str:
        filename = f"response_{uuid.uuid4().hex}.mp3"
        path = os.path.join("backend/audio", filename)

        os.makedirs("backend/audio", exist_ok=True)

        communicate = edge_tts.Communicate(text, self.voice)
        await communicate.save(path)

        return path