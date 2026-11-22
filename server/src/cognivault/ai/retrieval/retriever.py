import json
from pathlib import Path
from typing import Any

import faiss
import numpy as np

from cognivault.ai.embeddings import EmbeddingService


DEFAULT_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
EXPECTED_EMBEDDING_DIMENSION = 384


class SemanticRetriever:
    """Retrieve the most similar document chunks from a FAISS index."""

    def __init__(
        self,
        index_path: Path,
        metadata_path: Path,
        model_name: str = DEFAULT_MODEL_NAME,
    ) -> None:
        """Load the existing FAISS index and its chunk metadata."""
        if not index_path.is_file():
            raise FileNotFoundError(f"FAISS index file does not exist: {index_path}")
        if not metadata_path.is_file():
            raise FileNotFoundError(
                f"Chunk metadata file does not exist: {metadata_path}"
            )

        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        self.chunks: list[dict[str, Any]] = metadata.get("chunks")
        if not isinstance(self.chunks, list):
            raise ValueError("Chunk metadata must contain a 'chunks' list.")
        if not self.chunks:
            raise ValueError("Chunk metadata contains no chunks.")

        self.index = faiss.read_index(str(index_path))
        if self.index.ntotal != len(self.chunks):
            raise ValueError(
                f"FAISS index contains {self.index.ntotal} vectors but metadata "
                f"contains {len(self.chunks)} chunks."
            )
        if (
            "total_chunks" in metadata
            and metadata["total_chunks"] != len(self.chunks)
        ):
            raise ValueError(
                "Metadata 'total_chunks' does not match the number of chunks."
            )
        if self.index.d != EXPECTED_EMBEDDING_DIMENSION:
            raise ValueError(
                f"FAISS index dimension must be {EXPECTED_EMBEDDING_DIMENSION}, "
                f"got {self.index.d}."
            )
        if (
            "embedding_dimension" in metadata
            and metadata["embedding_dimension"] != EXPECTED_EMBEDDING_DIMENSION
        ):
            raise ValueError(
                "Metadata embedding_dimension must be "
                f"{EXPECTED_EMBEDDING_DIMENSION}, got "
                f"{metadata['embedding_dimension']}."
            )

        self.embedding_service = EmbeddingService(model_name)

    def search(self, query: str, top_k: int = 3) -> list[dict[str, Any]]:
        """Return up to top_k chunks ranked by cosine similarity."""
        if not isinstance(query, str) or not query.strip():
            raise ValueError("Query must not be empty.")
        if isinstance(top_k, bool) or not isinstance(top_k, int) or top_k <= 0:
            raise ValueError("top_k must be a positive integer.")

        query_embedding = np.asarray(
            self.embedding_service.generate_embeddings([query.strip()]),
            dtype=np.float32,
        )
        if query_embedding.shape != (1, EXPECTED_EMBEDDING_DIMENSION):
            raise ValueError(
                "Query embedding must have shape "
                f"(1, {EXPECTED_EMBEDDING_DIMENSION}), got "
                f"{query_embedding.shape}."
            )

        actual_top_k = min(top_k, self.index.ntotal)
        scores, indices = self.index.search(query_embedding, actual_top_k)

        results = []
        for score, index_position in zip(scores[0], indices[0]):
            if index_position < 0:
                continue

            chunk = self.chunks[int(index_position)]
            chunk_id = chunk.get("chunk_id") or chunk.get("id")
            results.append(
                {
                    "chunk_id": chunk_id,
                    "source": chunk.get("source"),
                    "chunk_index": self._get_chunk_index(chunk, chunk_id),
                    "text": chunk.get("text", ""),
                    "similarity_score": float(score),
                }
            )
        return results

    @staticmethod
    def _get_chunk_index(
        chunk: dict[str, Any], chunk_id: Any
    ) -> int | None:
        """Read a chunk index or derive it from the standard chunk identifier."""
        chunk_index = chunk.get("chunk_index")
        if isinstance(chunk_index, int) and not isinstance(chunk_index, bool):
            return chunk_index
        if isinstance(chunk_index, str) and chunk_index.isdigit():
            return int(chunk_index)

        if isinstance(chunk_id, str) and "_chunk_" in chunk_id:
            suffix = chunk_id.rsplit("_chunk_", 1)[1]
            if suffix.isdigit():
                return int(suffix)
        return None
