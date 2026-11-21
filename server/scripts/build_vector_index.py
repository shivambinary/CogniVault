import json
from pathlib import Path

import numpy as np

from cognivault.ai.retrieval.vector_store import FaissVectorStore


BASE_DIR = Path(__file__).resolve().parents[1]
EMBEDDINGS_PATH = BASE_DIR / "storage" / "embeddings" / "embeddings.npy"
EMBEDDING_METADATA_PATH = BASE_DIR / "storage" / "embeddings" / "metadata.json"
CHUNKS_PATH = BASE_DIR / "storage" / "chunks" / "chunks.json"
OUTPUT_DIR = BASE_DIR / "storage" / "vector_store"
INDEX_PATH = OUTPUT_DIR / "index.faiss"
CHUNKS_METADATA_PATH = OUTPUT_DIR / "chunks_metadata.json"


def main() -> None:
    input_paths = (
        (EMBEDDINGS_PATH, "Embeddings file"),
        (EMBEDDING_METADATA_PATH, "Embedding metadata file"),
        (CHUNKS_PATH, "Chunks file"),
    )
    for file_path, description in input_paths:
        if not file_path.exists():
            raise FileNotFoundError(f"{description} does not exist: {file_path}")

    embeddings = np.load(EMBEDDINGS_PATH)
    chunks = json.loads(CHUNKS_PATH.read_text(encoding="utf-8"))
    embedding_metadata = json.loads(
        EMBEDDING_METADATA_PATH.read_text(encoding="utf-8")
    )

    if len(chunks) != embeddings.shape[0]:
        raise ValueError(
            f"Chunk count ({len(chunks)}) does not match embedding count "
            f"({embeddings.shape[0]})."
        )

    chunk_ids = [chunk["chunk_id"] for chunk in chunks]
    if chunk_ids != embedding_metadata["chunk_ids"]:
        raise ValueError(
            "Chunk order does not match the embedding metadata. "
            "Regenerate embeddings before building the index."
        )

    vector_store = FaissVectorStore()
    index = vector_store.build_index(embeddings)
    vector_store.save_index(INDEX_PATH)

    chunks_metadata = {
        "total_chunks": len(chunks),
        "embedding_dimension": int(embeddings.shape[1]),
        "index_type": "IndexFlatIP",
        "distance_metric": "inner_product",
        "normalized_embeddings": True,
        "chunks": chunks,
    }
    CHUNKS_METADATA_PATH.write_text(
        json.dumps(chunks_metadata, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    index_info = vector_store.get_index_info()
    print(
        "Vector index built successfully.\n"
        f"Total vectors: {index_info['total_vectors']}\n"
        f"Vector dimension: {index_info['vector_dimension']}\n"
        f"Index type: {index_info['index_type']}\n"
        f"Index file: {INDEX_PATH}\n"
        f"Chunks metadata file: {CHUNKS_METADATA_PATH}"
    )


if __name__ == "__main__":
    main()
