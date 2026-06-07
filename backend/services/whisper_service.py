from faster_whisper import WhisperModel
import ffmpeg
import os
import logging

logger = logging.getLogger(__name__)

_model = None

def get_model():
    global _model
    if _model is None:
        logger.info("Loading Faster-Whisper model...")
        _model = WhisperModel("base", device="cpu", compute_type="int8")
    return _model

def extract_audio(video_path: str) -> str:
    audio_path = os.path.splitext(video_path)[0] + "_extracted.wav"
    try:
        (
            ffmpeg
            .input(video_path)
            .output(audio_path, acodec="pcm_s16le", ac=1, ar="16000")
            .overwrite_output()
            .run(quiet=True)
        )
        return audio_path
    except ffmpeg.Error as e:
        raise RuntimeError(f"Failed to extract audio: {e.stderr.decode()}")

def process_meeting_file(file_path: str) -> dict:
    ext = os.path.splitext(file_path)[1].lower()
    audio_path = file_path

    if ext == ".mp4":
        audio_path = extract_audio(file_path)

    model = get_model()
    segments, info = model.transcribe(audio_path, beam_size=5)

    full_text = " ".join([segment.text for segment in segments])

    if audio_path != file_path and os.path.exists(audio_path):
        os.remove(audio_path)

    return {
        "text": full_text.strip(),
        "language": info.language,
        "segments": [],
    }