from pathlib import Path

import faiss
import numpy as np


class FaissVectorStore:
    def __init__(self):
        self.index = None

    def build_index(self, embeddings: np.ndarray):
        embeddings = np.asarray(embeddings, dtype=np.float32)
        if embeddings.ndim != 2 or embeddings.shape[0] == 0:
            raise ValueError("embeddings must be a non-empty 2D array")
        if not np.isfinite(embeddings).all():
            raise ValueError("embeddings must contain only finite values")
        if not np.allclose(np.linalg.norm(embeddings, axis=1), 1.0, atol=1e-5):
            raise ValueError("each embedding must have an L2 norm close to 1.0")

        self.index = faiss.IndexFlatIP(embeddings.shape[1])
        self.index.add(embeddings)
        return self.index

    def save_index(self, file_path: Path):
        if self.index is None:
            raise RuntimeError("No index has been built or loaded")
        file_path.parent.mkdir(parents=True, exist_ok=True)
        faiss.write_index(self.index, str(file_path))

    def load_index(self, file_path: Path):
        if not file_path.exists():
            raise FileNotFoundError(file_path)
        self.index = faiss.read_index(str(file_path))
        return self.index

    def get_index_info(self) -> dict:
        if self.index is None:
            raise RuntimeError("No index has been built or loaded")
        return {
            "total_vectors": self.index.ntotal,
            "vector_dimension": self.index.d,
            "index_type": type(self.index).__name__,
        }
