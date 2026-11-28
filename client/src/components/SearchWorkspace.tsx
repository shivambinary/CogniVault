
import {
  ArrowUp,
  Sparkles,
  FileText,
  ShieldCheck,
  Users,
  House,
  Search,
} from "lucide-react";

import { useEffect, useRef } from "react";
import SearchResults from "./SearchResults";
import type { ChatMessage } from "../types/search";

interface SearchWorkspaceProps {
  query: string;
  setQuery: (value: string) => void;
  onSearch: (value?: string) => void;
  messages: ChatMessage[];
  loading: boolean;
}

const suggestions = [
  {
    title: "Leave & benefits",
    description: "What is the company's leave policy?",
    icon: FileText,
  },
  {
    title: "Remote work",
    description: "What are the work-from-home rules?",
    icon: House,
  },
  {
    title: "IT & security",
    description: "What are the password security guidelines?",
    icon: ShieldCheck,
  },
  {
    title: "HR information",
    description: "How does employee onboarding work?",
    icon: Users,
  },
];

export default function SearchWorkspace({
  query,
  setQuery,
  onSearch,
  messages,
  loading,
}: SearchWorkspaceProps) {
  const hasMessages = messages.length > 0;

  const latestQueryRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    latestQueryRef.current?.scrollIntoView({
      behavior: "smooth",
      block: "start",
    });
  }, [messages.length]);

  return (
    <main className="workspace">
      <header className="workspace-header">
        <div className="workspace-header-label">
          <Sparkles size={15} />
          <span>KNOWLEDGE INTELLIGENCE</span>
        </div>

        <div className="workspace-status">
          <span className="status-dot" />
          Search workspace
        </div>
      </header>

      <div
        className={`workspace-content ${
          hasMessages ? "workspace-searched" : ""
        }`}
      >
        {!hasMessages ? (
          <div className="welcome-section">
            <div className="welcome-icon">
              <Sparkles size={22} />
            </div>

            <div className="welcome-eyebrow">
              YOUR COMPANY KNOWLEDGE, CONNECTED
            </div>

            <h1>
              What do you want
              <br />
              <span>to know today?</span>
            </h1>

            <p className="welcome-description">
              Search across your organization's knowledge and discover
              relevant information in seconds.
            </p>

            <div className="suggestion-grid">
              {suggestions.map((suggestion) => {
                const Icon = suggestion.icon;

                return (
                  <button
                    className="suggestion-card"
                    key={suggestion.title}
                    onClick={() =>
                      onSearch(suggestion.description)
                    }
                    disabled={loading}
                  >
                    <div className="suggestion-icon">
                      <Icon size={18} />
                    </div>

                    <div className="suggestion-content">
                      <span className="suggestion-title">
                        {suggestion.title}
                      </span>

                      <span className="suggestion-description">
                        {suggestion.description}
                      </span>
                    </div>
                  </button>
                );
              })}
            </div>
          </div>
        ) : (
          <div className="chat-thread">
            {messages.map((message, index) => (
              <div
                className="chat-message"
                key={message.id}
              >
                {/* User query */}

                <div
                  className="user-query"
                  ref={
                    index === messages.length - 1
                      ? latestQueryRef
                      : undefined
                  }
                >
                  <div className="query-avatar">Y</div>

                  <div className="query-bubble">
                    {message.query}
                  </div>
                </div>

                {/* CogniVault response */}

                <div className="response-heading">
                  <div className="assistant-avatar">
                    <Sparkles size={18} />
                  </div>

                  <div className="response-heading-content">
                    <span className="assistant-name">
                      CogniVault
                    </span>

                    <span className="response-subtitle">
                      Semantic knowledge search
                    </span>
                  </div>
                </div>

                {/* Loading */}

                {message.loading ? (
                  <div className="loading-state">
                    <div className="loading-indicator">
                      <span />
                      <span />
                      <span />
                    </div>

                    <p>
                      Searching your knowledge base...
                    </p>
                  </div>
                ) : message.error ? (
                  /* Error */

                  <div className="search-error">
                    <strong>
                      Search couldn't be completed
                    </strong>

                    <p>{message.error}</p>

                    <p>
                      Check that the CogniVault backend is running
                      and try again.
                    </p>
                  </div>
                ) : (
                  /* Results */

                  <>
                    <div className="results-intro">
                      <div className="results-intro-icon">
                        <Search size={16} />
                      </div>

                      <div>
                        <h2>
                          {message.results.length} relevant{" "}
                          {message.results.length === 1
                            ? "passage"
                            : "passages"}{" "}
                          found
                        </h2>

                        <p>
                          Here are the document excerpts most
                          relevant to your question.
                        </p>
                      </div>
                    </div>

                    {message.results.length > 0 ? (
                      <SearchResults
                        results={message.results}
                      />
                    ) : (
                      <div className="no-results">
                        <Search size={22} />

                        <h3>
                          No relevant passages found
                        </h3>

                        <p>
                          Try rephrasing your question.
                        </p>
                      </div>
                    )}
                  </>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Input */}

      <div className="search-input-container">
        <form
          className="search-input-box"
          onSubmit={(event) => {
            event.preventDefault();

            if (!query.trim() || loading) return;

            onSearch(query);
          }}
        >
          <textarea
            value={query}
            onChange={(event) =>
              setQuery(event.target.value)
            }
            placeholder="Ask anything about your company..."
            rows={1}
            onKeyDown={(event) => {
              if (
                event.key === "Enter" &&
                !event.shiftKey
              ) {
                event.preventDefault();

                if (!query.trim() || loading) return;

                onSearch(query);
              }
            }}
          />

          <div className="search-input-footer">
            <div className="input-hint">
              <Sparkles size={14} />

              <span>
                Search company knowledge
              </span>
            </div>

            <button
              type="submit"
              className="submit-search"
              disabled={!query.trim() || loading}
              title="Search"
            >
              <ArrowUp size={18} />
            </button>
          </div>
        </form>

        <p className="input-disclaimer">
          CogniVault retrieves relevant passages from your knowledge base.
        </p>
      </div>
    </main>
  );
}
