import os
import logging
from groq import Groq

logger = logging.getLogger(__name__)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def process_meeting_file(file_path: str) -> dict:
    """
    Transcribe audio/video using Groq's Whisper API.
    Runs on Groq's servers — no local RAM used at all.
    """
    logger.info(f"Sending file to Groq Whisper: {file_path}")

    with open(file_path, "rb") as f:
        transcription = client.audio.transcriptions.create(
            file=(os.path.basename(file_path), f),
            model="whisper-large-v3",
            response_format="verbose_json",
        )

    return {
        "text": transcription.text.strip(),
        "language": getattr(transcription, "language", "unknown"),
        "segments": [],
    }