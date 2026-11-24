
import json
from pathlib import Path

from cognivault.ai.retrieval.retriever import SemanticRetriever
from cognivault.ai.evaluation.evaluator import RetrievalEvaluator


BASE_DIR = Path(__file__).resolve().parents[1]

INDEX_PATH = BASE_DIR / "storage" / "vector_store" / "index.faiss"

METADATA_PATH = (
    BASE_DIR / "storage" / "vector_store" / "chunks_metadata.json"
)

DATASET_PATH = (
    BASE_DIR / "data" / "evaluation_dataset" / "questions.json"
)

OUTPUT_PATH = (
    BASE_DIR / "storage" / "evaluation_results.json"
)

TOP_K = 3


def main():

    # Load evaluation questions
    dataset = json.loads(
        DATASET_PATH.read_text(encoding="utf-8")
    )

    # Load retrieval engine
    retriever = SemanticRetriever(
        index_path=INDEX_PATH,
        metadata_path=METADATA_PATH
    )

    # Evaluate retrieval
    evaluator = RetrievalEvaluator(retriever)

    report = evaluator.evaluate_dataset(
        dataset=dataset,
        top_k=TOP_K
    )

    # Save evaluation report
    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    OUTPUT_PATH.write_text(
        json.dumps(report, indent=4, ensure_ascii=False),
        encoding="utf-8"
    )

    # Display results
    print("\nCogniVault Retrieval Evaluation")
    print("=" * 45)

    for result in report["question_results"]:

        print("\nQuestion:", result["question"])

        print("Expected:", result["expected_sources"])

        print("Retrieved:", result["retrieved_sources"])

        print(
            "Precision@K:",
            round(result["precision_at_k"], 3)
        )

        print(
            "Recall@K:",
            round(result["recall_at_k"], 3)
        )

        print(
            "Hit Rate@K:",
            round(result["hit_rate_at_k"], 3)
        )

    print("\nOverall Results")
    print("-" * 45)

    print(
        "Average Precision@K:",
        round(report["average_precision_at_k"], 3)
    )

    print(
        "Average Recall@K:",
        round(report["average_recall_at_k"], 3)
    )

    print(
        "Average Hit Rate@K:",
        round(report["average_hit_rate_at_k"], 3)
    )

    print("\nEvaluation report saved:", OUTPUT_PATH)


if __name__ == "__main__":
    main()