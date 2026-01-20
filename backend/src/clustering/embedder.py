from typing import List, Union
from ..core.model_registry import ModelRegistry, AbstractModel
from ..config.settings import get_settings

settings = get_settings()

@ModelRegistry.register("embedder")
class EmbedderService(AbstractModel):
    def __init__(self):
        from sentence_transformers import SentenceTransformer
        # Load multilingual model for Indic language support
        self.model = SentenceTransformer(settings.EMBEDDING_MODEL)

    def predict(self, text: Union[str, List[str]]) -> Any:
        """
        Generate embeddings for text or list of texts.
        Returns numpy array or list of arrays.
        """
        if isinstance(text, str):
            text = [text]
            
        embeddings = self.model.encode(text, show_progress_bar=False)
        
        # If input was single string, return single embedding
        if len(text) == 1:
            return embeddings[0]
            
        return embeddings
