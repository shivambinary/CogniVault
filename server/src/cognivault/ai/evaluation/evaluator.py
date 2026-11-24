
class RetrievalEvaluator:
    """
    Evaluates retrieval quality using expected document sources.
    """

    def __init__(self, retriever):
        self.retriever = retriever

    def evaluate_question(
        self,
        question: str,
        expected_sources: list[str],
        top_k: int = 3
    ) -> dict:

        results = self.retriever.search(
            query=question,
            top_k=top_k
        )

        # Count each source document only once
        retrieved_sources = []

        for result in results:
            source = result["source"]

            if source not in retrieved_sources:
                retrieved_sources.append(source)

        expected = set(expected_sources)
        retrieved = set(retrieved_sources)

        relevant_found = expected.intersection(retrieved)

        # Precision@K uses K as its denominator
        precision = len(relevant_found) / top_k

        # Recall@K measures how many expected sources were found
        recall = (
            len(relevant_found) / len(expected)
            if expected else 0.0
        )

        hit_rate = 1.0 if relevant_found else 0.0

        return {
            "question": question,
            "expected_sources": sorted(expected),
            "retrieved_sources": retrieved_sources,
            "relevant_found": sorted(relevant_found),
            "precision_at_k": precision,
            "recall_at_k": recall,
            "hit_rate_at_k": hit_rate
        }

    def evaluate_dataset(
        self,
        dataset: list[dict],
        top_k: int = 3
    ) -> dict:

        if not dataset:
            raise ValueError("Evaluation dataset is empty.")

        results = []

        for item in dataset:

            result = self.evaluate_question(
                question=item["question"],
                expected_sources=item["expected_sources"],
                top_k=top_k
            )

            results.append(result)

        count = len(results)

        return {
            "total_questions": count,
            "top_k": top_k,
            "average_precision_at_k": sum(
                item["precision_at_k"] for item in results
            ) / count,
            "average_recall_at_k": sum(
                item["recall_at_k"] for item in results
            ) / count,
            "average_hit_rate_at_k": sum(
                item["hit_rate_at_k"] for item in results
            ) / count,
            "question_results": results
        }