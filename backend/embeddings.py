from sentence_transformers import SentenceTransformer
from backend.config import EMBEDDING_MODEL

class Embedder:
    _model = None 
    def __init__(self):
        if Embedder._model is None:
            Embedder._model = SentenceTransformer(
                EMBEDDING_MODEL,
                device="cpu" 
            )
        self.model = Embedder._model
    def embed(self, text: str):
        return self.model.encode(text).tolist()
