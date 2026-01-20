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
        device = "cuda" if settings.ASR_GPU_ENABLED else "cpu"
        compute_type = "float16" if settings.ASR_GPU_ENABLED else "int8"
        
        self.model = WhisperModel(settings.WHISPER_MODEL, device=device, compute_type=compute_type)


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
