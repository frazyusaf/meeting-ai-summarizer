import whisper
import ffmpeg
import os
import logging

logger = logging.getLogger(__name__)

# Load model once at startup — avoids reloading on every request
_model = None


def get_model(size: str = "base"):
    """Lazy-load the Whisper model (cached after first load)."""
    global _model
    if _model is None:
        logger.info(f"Loading Whisper model: {size}")
        _model = whisper.load_model(size)
    return _model


def extract_audio(video_path: str) -> str:
    """
    Extract audio track from a video file using FFmpeg.
    Returns path to the extracted .wav file.
    """
    audio_path = os.path.splitext(video_path)[0] + "_extracted.wav"
    try:
        (
            ffmpeg
            .input(video_path)
            .output(audio_path, acodec="pcm_s16le", ac=1, ar="16000")
            .overwrite_output()
            .run(quiet=True)
        )
        logger.info(f"Audio extracted to {audio_path}")
        return audio_path
    except ffmpeg.Error as e:
        logger.error(f"FFmpeg error: {e.stderr.decode()}")
        raise RuntimeError(f"Failed to extract audio: {e.stderr.decode()}")


def transcribe_audio(file_path: str, model_size: str = "base") -> dict:
    """
    Transcribe audio file to text using OpenAI Whisper.

    Returns:
        dict with keys: text, segments, language
    """
    model = get_model(model_size)

    logger.info(f"Starting transcription for: {file_path}")
    result = model.transcribe(file_path, verbose=False)

    return {
        "text": result["text"].strip(),
        "segments": result.get("segments", []),
        "language": result.get("language", "unknown"),
    }


def process_meeting_file(file_path: str) -> dict:
    """
    Full pipeline: handle both audio and video inputs.
    Extracts audio if needed, then transcribes.
    """
    ext = os.path.splitext(file_path)[1].lower()
    audio_path = file_path

    if ext == ".mp4":
        audio_path = extract_audio(file_path)

    result = transcribe_audio(audio_path)

    # Clean up extracted audio file if it was created
    if audio_path != file_path and os.path.exists(audio_path):
        os.remove(audio_path)

    return result
