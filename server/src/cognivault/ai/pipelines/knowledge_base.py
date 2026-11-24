
import json
from pathlib import Path

import numpy as np

from cognivault.ai.ingestion.parser import parse_document
from cognivault.ai.chunking.splitter import split_text
from cognivault.ai.embeddings.embedding_service import EmbeddingService
from cognivault.ai.retrieval.vector_store import FaissVectorStore


class KnowledgeBasePipeline:
    """
    Builds CogniVault's searchable knowledge base
    from the original company documents.
    """

    def __init__(
        self,
        documents_dir: Path,
        storage_dir: Path,
        chunk_size: int = 150,
        chunk_overlap: int = 30
    ):
        self.documents_dir = documents_dir
        self.storage_dir = storage_dir

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        self.embedding_service = EmbeddingService()

    def load_and_chunk_documents(self) -> list[dict]:

        all_chunks = []

        supported_extensions = {".txt", ".pdf", ".docx"}

        files = sorted(
            path for path in self.documents_dir.iterdir()
            if path.is_file()
            and path.suffix.lower() in supported_extensions
        )

        if not files:
            raise FileNotFoundError("No supported documents found.")

        for file_path in files:

            document = parse_document(file_path)

            text = document["text"]

            if not text.strip():
                print(f"Skipping empty document: {file_path.name}")
                continue

            text_chunks = split_text(
                text,
                chunk_size=self.chunk_size,
                overlap=self.chunk_overlap
            )

            for index, chunk_text in enumerate(text_chunks):

                all_chunks.append({
                    "chunk_id": f"{file_path.name}_chunk_{index}",
                    "source": file_path.name,
                    "chunk_index": index,
                    "text": chunk_text,
                    "word_count": len(chunk_text.split())
                })

            print(
                f"Processed {file_path.name}: "
                f"{len(text_chunks)} chunks"
            )

        if not all_chunks:
            raise ValueError("No usable document chunks were generated.")

        return all_chunks

    def generate_embeddings(self, chunks: list[dict]) -> np.ndarray:

        texts = [chunk["text"] for chunk in chunks]

        return self.embedding_service.generate_embeddings(texts)

    def save_artifacts(
        self,
        chunks: list[dict],
        embeddings: np.ndarray
    ):

        chunks_dir = self.storage_dir / "chunks"
        embeddings_dir = self.storage_dir / "embeddings"
        vector_dir = self.storage_dir / "vector_store"

        chunks_dir.mkdir(parents=True, exist_ok=True)
        embeddings_dir.mkdir(parents=True, exist_ok=True)
        vector_dir.mkdir(parents=True, exist_ok=True)

        # Save chunks
        (chunks_dir / "chunks.json").write_text(
            json.dumps(chunks, indent=4, ensure_ascii=False),
            encoding="utf-8"
        )

        # Save embeddings
        np.save(
            embeddings_dir / "embeddings.npy",
            embeddings
        )

        embedding_metadata = {
            "model": self.embedding_service.model_name,
            "total_chunks": len(chunks),
            "embedding_dimension": int(embeddings.shape[1]),
            "normalized": True,
            "chunk_ids": [
                chunk["chunk_id"] for chunk in chunks
            ]
        }

        (embeddings_dir / "metadata.json").write_text(
            json.dumps(embedding_metadata, indent=4),
            encoding="utf-8"
        )

        # Build and save FAISS index
        vector_store = FaissVectorStore()

        vector_store.build_index(embeddings)

        vector_store.save_index(
            vector_dir / "index.faiss"
        )

        # Save chunk metadata in vector order
        vector_metadata = {
            "total_chunks": len(chunks),
            "embedding_dimension": int(embeddings.shape[1]),
            "index_type": "IndexFlatIP",
            "distance_metric": "inner_product",
            "normalized_embeddings": True,
            "chunks": chunks
        }

        (vector_dir / "chunks_metadata.json").write_text(
            json.dumps(vector_metadata, indent=4, ensure_ascii=False),
            encoding="utf-8"
        )

    def build(self):

        print("\nCogniVault Knowledge Base Builder")
        print("=" * 45)

        # Step 1: Load and chunk documents
        print("\n[1/4] Loading and chunking documents...")

        chunks = self.load_and_chunk_documents()

        print(f"Total chunks created: {len(chunks)}")

        # Step 2: Generate embeddings
        print("\n[2/4] Generating embeddings...")

        embeddings = self.generate_embeddings(chunks)

        print(f"Embedding shape: {embeddings.shape}")

        # Step 3: Save vectors and index
        print("\n[3/4] Building and saving FAISS index...")

        self.save_artifacts(chunks, embeddings)

        # Step 4: Report
        print("\n[4/4] Knowledge base build completed!")

        print(f"Documents directory: {self.documents_dir}")
        print(f"Total chunks: {len(chunks)}")
        print(f"Vector dimension: {embeddings.shape[1]}")

        return {
            "total_chunks": len(chunks),
            "embedding_dimension": int(embeddings.shape[1])
        }