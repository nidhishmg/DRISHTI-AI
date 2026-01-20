import os
import argparse
# import spacy
from sentence_transformers import SentenceTransformer
from faster_whisper import WhisperModel
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
# from config.settings import get_settings (Importing relative might fail in script mode without path hack)

# Hardcoding defaults for script robustness
MODELS_DIR = "/models"
WHISPER_MODEL = "faster-whisper-medium"
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
NER_MODEL = "xx_ent_wiki_sm"

def download_models():
    print(f"Starting model download to {MODELS_DIR}...")
    os.makedirs(MODELS_DIR, exist_ok=True)

    # 1. Whisper
    print(f"Downloading Whisper: {WHISPER_MODEL}")
    try:
        WhisperModel(WHISPER_MODEL, download_root=os.path.join(MODELS_DIR, "whisper"))
        print("Whisper downloaded.")
    except Exception as e:
        print(f"Failed to download Whisper: {e}")

    # 2. Embeddings
    print(f"Downloading Embeddings: {EMBEDDING_MODEL}")
    try:
        SentenceTransformer(EMBEDDING_MODEL, cache_folder=os.path.join(MODELS_DIR, "embeddings"))
        print("Embeddings downloaded.")
    except Exception as e:
        print(f"Failed to download Embeddings: {e}")

    # 3. SpaCy
    print(f"Downloading SpaCy: {NER_MODEL}")
    try:
        os.system(f"python -m spacy download {NER_MODEL}")
        print("SpaCy model downloaded.")
    except Exception as e:
        print(f"Failed to download SpaCy: {e}")

    print("All models processed.")

if __name__ == "__main__":
    download_models()
