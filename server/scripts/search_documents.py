from pathlib import Path

from cognivault.ai.retrieval.retriever import SemanticRetriever


BASE_DIR = Path(__file__).resolve().parents[1]
INDEX_PATH = BASE_DIR / "storage" / "vector_store" / "index.faiss"
METADATA_PATH = BASE_DIR / "storage" / "vector_store" / "chunks_metadata.json"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def main() -> None:
    """Run an interactive semantic search over the indexed documents."""
    try:
        retriever = SemanticRetriever(
            index_path=INDEX_PATH,
            metadata_path=METADATA_PATH,
            model_name=MODEL_NAME,
        )
    except Exception as error:
        print(f"Unable to initialize semantic search: {error}")
        return

    print("Semantic document search. Enter 'exit' or 'quit' to stop.")
    while True:
        try:
            query = input("\nQuestion: ")
        except (EOFError, KeyboardInterrupt):
            print("\nExiting semantic search.")
            return

        if query.strip().lower() in {"exit", "quit"}:
            print("Exiting semantic search.")
            return
        if not query.strip():
            print("Please enter a question.")
            continue

        try:
            results = retriever.search(query, top_k=3)
        except Exception as error:
            print(f"Search failed: {error}")
            continue

        if not results:
            print("No matching document chunks found.")
            continue

        for rank, result in enumerate(results, start=1):
            print(
                f"\nResult {rank}\n"
                f"Source: {result['source']}\n"
                f"Chunk ID: {result['chunk_id']}\n"
                f"Similarity score: {result['similarity_score']:.4f}\n"
                f"Content: {result['text']}"
            )


if __name__ == "__main__":
    main()
