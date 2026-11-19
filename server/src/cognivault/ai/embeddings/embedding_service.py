import numpy as np
from sentence_transformers import SentenceTransformer


class EmbeddingService:
    def __init__(
        self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    ) -> None:
        print(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        print("Embedding model loaded successfully.")

    def generate_embeddings(self, texts: list[str]) -> np.ndarray:
        if not texts:
            raise ValueError("Cannot generate embeddings for empty text.")

        return self.model.encode(
            texts,
            batch_size=32,
            show_progress_bar=True,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )
