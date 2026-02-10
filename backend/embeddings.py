from sentence_transformers import SentenceTransformer
from backend.config import EMBEDDING_MODEL

class Embedder:
    _model = None  # class-level cache

    def __init__(self):
        if Embedder._model is None:
            Embedder._model = SentenceTransformer(
                EMBEDDING_MODEL,
                device="cpu"   # 🔑 force CPU, avoid meta tensors
            )

        self.model = Embedder._model

    def embed(self, text: str):
        return self.model.encode(text).tolist()
