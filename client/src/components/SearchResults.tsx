
import { useState } from "react";
import { FileText, Copy, Check, ChevronDown, ChevronUp } from "lucide-react";
import type { SearchResult } from "../types/search";

interface SearchResultsProps {
  results: SearchResult[];
}

export default function SearchResults({ results }: SearchResultsProps) {
  const [expandedIds, setExpandedIds] = useState<string[]>([]);
  const [copiedId, setCopiedId] = useState<string | null>(null);

  function toggleExpanded(id: string) {
    setExpandedIds((current) =>
      current.includes(id)
        ? current.filter((item) => item !== id)
        : [...current, id]
    );
  }

  async function copyText(result: SearchResult) {
    try {
      await navigator.clipboard.writeText(result.text);
      setCopiedId(result.id);

      window.setTimeout(() => {
        setCopiedId(null);
      }, 1500);
    } catch {
      setCopiedId(null);
    }
  }

  return (
    <div className="results-list">
      {results.map((result, index) => {
        const expanded = expandedIds.includes(result.id);
        const copied = copiedId === result.id;

        return (
          <article className="result-card" key={result.id}>
            <div className="result-card-header">
              <div className="source-info">
                <div className="source-icon">
                  <FileText size={17} />
                </div>

                <div className="source-details">
                  <span className="source-name" title={result.source}>
                    {result.source}
                  </span>
                  <span className="source-label">Knowledge base document</span>
                </div>
              </div>

              <span className="result-number">
                #{index + 1}
              </span>
            </div>

            <div className="result-score-row">
              <div className="score-label">
                <span>Relevance</span>
                <strong>{Math.round(result.score * 100)}%</strong>
              </div>

              <div className="score-track">
                <div
                  className="score-fill"
                  style={{ width: `${result.score * 100}%` }}
                />
              </div>
            </div>

            <div className={`passage ${expanded ? "" : "passage-collapsed"}`}>
              {result.text}
            </div>

            <div className="result-actions">
              <button
                className="text-button"
                onClick={() => toggleExpanded(result.id)}
              >
                {expanded ? (
                  <>
                    Show less <ChevronUp size={15} />
                  </>
                ) : (
                  <>
                    Read full passage <ChevronDown size={15} />
                  </>
                )}
              </button>

              <button
                className="text-button copy-button"
                onClick={() => copyText(result)}
              >
                {copied ? (
                  <>
                    <Check size={15} /> Copied
                  </>
                ) : (
                  <>
                    <Copy size={15} /> Copy
                  </>
                )}
              </button>
            </div>
          </article>
        );
      })}
    </div>
  );
}
