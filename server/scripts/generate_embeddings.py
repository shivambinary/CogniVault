import json
from pathlib import Path

import numpy as np

from cognivault.ai.embeddings import EmbeddingService


BASE_DIR = Path(__file__).resolve().parents[1]
CHUNKS_PATH = BASE_DIR / "storage" / "chunks" / "chunks.json"
OUTPUT_DIR = BASE_DIR / "storage" / "embeddings"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def main() -> None:
    if not CHUNKS_PATH.exists():
        raise FileNotFoundError(f"Chunks file does not exist: {CHUNKS_PATH}")
    if CHUNKS_PATH.stat().st_size == 0:
        raise ValueError(f"Chunks file is empty: {CHUNKS_PATH}")

    chunks = json.loads(CHUNKS_PATH.read_text(encoding="utf-8"))
    if not chunks:
        raise ValueError(f"No chunks found in {CHUNKS_PATH}")

    texts = [chunk["text"] for chunk in chunks]
    chunk_ids = [chunk["id"] for chunk in chunks]
    embedding_service = EmbeddingService(MODEL_NAME)
    embeddings = embedding_service.generate_embeddings(texts)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    np.save(OUTPUT_DIR / "embeddings.npy", embeddings)

    metadata = {
        "model": MODEL_NAME,
        "total_chunks": len(chunks),
        "embedding_dimension": int(embeddings.shape[1]),
        "normalized": True,
        "chunk_ids": chunk_ids,
    }
    (OUTPUT_DIR / "metadata.json").write_text(
        json.dumps(metadata, indent=2),
        encoding="utf-8",
    )
    print(f"Saved embeddings for {len(chunks)} chunks to {OUTPUT_DIR}.")


if __name__ == "__main__":
    main()
