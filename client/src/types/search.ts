export interface SearchResult {
  id: string;
  source: string;
  text: string;
  score: number;
}

export interface SearchResponse {
  query: string;
  results: SearchResult[];
}

export interface Conversation {
  id: string;
  title: string;
}

export interface ChatMessage {
  id: string;
  query: string;
  results: SearchResult[];
  loading: boolean;
  error: string | null;
}