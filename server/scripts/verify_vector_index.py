import json
from pathlib import Path

from cognivault.ai.retrieval.vector_store import FaissVectorStore


BASE_DIR = Path(__file__).resolve().parents[1]
INDEX_FILE = BASE_DIR / "storage" / "vector_store" / "index.faiss"
METADATA_FILE = BASE_DIR / "storage" / "vector_store" / "chunks_metadata.json"


def main() -> None:
    metadata = json.loads(METADATA_FILE.read_text(encoding="utf-8"))
    vector_store = FaissVectorStore()
    vector_store.load_index(INDEX_FILE)
    info = vector_store.get_index_info()

    print(f"Index type: {info['index_type']}")
    print(f"Total vectors: {info['total_vectors']}")
    print(f"Vector dimension: {info['vector_dimension']}")
    print(f"Metadata chunk count: {metadata['total_chunks']}")

    assert info["total_vectors"] == metadata["total_chunks"]
    assert info["vector_dimension"] == metadata["embedding_dimension"]
    assert len(metadata["chunks"]) == info["total_vectors"]

    print("FAISS index verification successful!")


if __name__ == "__main__":
    main()
