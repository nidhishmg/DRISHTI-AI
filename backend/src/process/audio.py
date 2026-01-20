import os
from ..core.model_registry import ModelRegistry, AbstractModel
from ..config.settings import get_settings
# import faster_whisper # Lazy import to avoid load time on startup if not needed

settings = get_settings()

@ModelRegistry.register("whisper")
class WhisperAudioProcessor(AbstractModel):
    def __init__(self):
        from faster_whisper import WhisperModel
        # Use settings for model size and compute type
        # "int8" is safer for CPU/low-memory GPU
        self.model = WhisperModel(settings.WHISPER_MODEL, device="auto", compute_type="int8")

    def predict(self, file_path: str) -> dict:
        """
        Transcribe audio file.
        Returns dict with 'text', 'language', 'confidence'.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Audio file not found: {file_path}")

        segments, info = self.model.transcribe(file_path, beam_size=5)
        
        # Combine segments
        full_text = " ".join([segment.text for segment in segments])
        
        return {
            "text": full_text.strip(),
            "language": info.language,
            "language_probability": info.language_probability,
            "duration": info.duration
        }
