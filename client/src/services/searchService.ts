import type { SearchResult } from "../types/search";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

interface BackendSearchResult {
  chunk_id: string | null;
  source: string | null;
  chunk_index: number | null;
  text: string;
  similarity_score: number;
}

interface BackendSearchResponse {
  query: string;
  total_results: number;
  results: BackendSearchResult[];
}

export async function searchKnowledgeBase(
  query: string,
  topK: number = 3
): Promise<SearchResult[]> {
  const response = await fetch(`${API_BASE_URL}/api/search`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      query,
      top_k: topK,
    }),
  });

  if (!response.ok) {
    let message = `Search failed (${response.status})`;

    try {
      const errorData = await response.json();
      if (errorData.detail) {
        message = errorData.detail;
      }
    } catch {
      // Keep the default error message.
    }

    throw new Error(message);
  }

  const data: BackendSearchResponse = await response.json();

  return data.results.map((result, index) => ({
    id: result.chunk_id ?? `result-${index}`,
    source: result.source ?? "Unknown source",
    text: result.text,
    score: result.similarity_score,
  }));
}