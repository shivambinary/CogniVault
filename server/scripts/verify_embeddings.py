import json
from pathlib import Path

import numpy as np


BASE_DIR = Path(__file__).resolve().parents[1]
EMBEDDINGS_PATH = BASE_DIR / "storage" / "embeddings" / "embeddings.npy"
METADATA_PATH = BASE_DIR / "storage" / "embeddings" / "metadata.json"


def main() -> None:
    embeddings = np.load(EMBEDDINGS_PATH)
    metadata = json.loads(METADATA_PATH.read_text(encoding="utf-8"))

    print(f"Embedding shape: {embeddings.shape}")
    print(f"Metadata: {json.dumps(metadata, indent=2)}")

    valid_shape = embeddings.ndim == 2 and embeddings.shape[0] > 0
    first_values = embeddings[0, :10] if valid_shape else np.array([])
    print(f"First 10 values of the first vector: {first_values}")

    finite = bool(np.isfinite(embeddings).all())
    print(f"All embedding values are finite: {finite}")

    norms = np.linalg.norm(embeddings, axis=1) if valid_shape else np.array([])
    unit_norms = bool(
        valid_shape and np.allclose(norms, 1.0, atol=1e-5)
    )
    print(f"All L2 norms are close to 1.0: {unit_norms}")

    metadata_matches = (
        metadata.get("total_chunks") == embeddings.shape[0]
        and metadata.get("embedding_dimension") == embeddings.shape[1]
    ) if valid_shape else False
    if not (valid_shape and finite and unit_norms and metadata_matches):
        raise ValueError("Embedding verification failed.")

    print("Embedding verification passed.")


if __name__ == "__main__":
    main()
