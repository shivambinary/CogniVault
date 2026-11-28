import { useState } from "react";
import Sidebar from "./components/Sidebar";
import SearchWorkspace from "./components/SearchWorkspace";
import { searchKnowledgeBase } from "./services/searchService";
import type { ChatMessage, Conversation } from "./types/search";

interface SavedConversation {
  conversation: Conversation;
  messages: ChatMessage[];
}

export default function App() {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [loading, setLoading] = useState(false);
  const [collapsed, setCollapsed] = useState(false);

  const [activeConversationId, setActiveConversationId] = useState<
    string | null
  >(null);

  const [conversations, setConversations] = useState<SavedConversation[]>([]);

  // --------------------------------------------------
  // Search knowledge base and append to current thread
  // --------------------------------------------------

  const handleSearch = async (searchQuery?: string) => {
    const trimmedQuery = searchQuery?.trim() ?? "";

    if (!trimmedQuery || loading) return;

    setQuery("");
    setLoading(true);

    let conversationId = activeConversationId;

    // Create a conversation if one is not currently active.
    if (!conversationId) {
      conversationId = crypto.randomUUID();

      const newConversation: SavedConversation = {
        conversation: {
          id: conversationId,
          title: trimmedQuery,
        },
        messages: [],
      };

      setConversations((previous) => [
        newConversation,
        ...previous,
      ]);

      setActiveConversationId(conversationId);
    }

    const messageId = crypto.randomUUID();

    const newMessage: ChatMessage = {
      id: messageId,
      query: trimmedQuery,
      results: [],
      loading: true,
      error: null,
    };

    // Append the query immediately to the active conversation.
    setMessages((previous) => [
      ...previous,
      newMessage,
    ]);

    // Update saved conversation history as well.
    setConversations((previous) =>
      previous.map((item) =>
        item.conversation.id === conversationId
          ? {
              ...item,
              messages: [...item.messages, newMessage],
            }
          : item
      )
    );

    try {
      const searchResults = await searchKnowledgeBase(trimmedQuery, 3);

      const completedMessage: ChatMessage = {
        ...newMessage,
        results: searchResults,
        loading: false,
        error: null,
      };

      // Update current thread.
      setMessages((previous) =>
        previous.map((message) =>
          message.id === messageId
            ? completedMessage
            : message
        )
      );

      // Update stored thread.
      setConversations((previous) =>
        previous.map((item) =>
          item.conversation.id === conversationId
            ? {
                ...item,
                messages: item.messages.map((message) =>
                  message.id === messageId
                    ? completedMessage
                    : message
                ),
              }
            : item
        )
      );
    } catch (error) {
      console.error("Search error:", error);

      const failedMessage: ChatMessage = {
        ...newMessage,
        loading: false,
        error:
          error instanceof Error
            ? error.message
            : "Something went wrong while searching.",
      };

      setMessages((previous) =>
        previous.map((message) =>
          message.id === messageId
            ? failedMessage
            : message
        )
      );

      setConversations((previous) =>
        previous.map((item) =>
          item.conversation.id === conversationId
            ? {
                ...item,
                messages: item.messages.map((message) =>
                  message.id === messageId
                    ? failedMessage
                    : message
                ),
              }
            : item
        )
      );
    } finally {
      setLoading(false);
    }
  };

  // --------------------------------------------------
  // Start a fresh conversation
  // --------------------------------------------------

  function handleNewConversation() {
    setQuery("");
    setMessages([]);
    setLoading(false);
    setActiveConversationId(null);
  }

  // --------------------------------------------------
  // Restore an existing conversation
  // --------------------------------------------------

  function handleSelectConversation(id: string) {
    const selected = conversations.find(
      (item) => item.conversation.id === id
    );

    if (!selected) return;

    setQuery("");
    setMessages(selected.messages);
    setActiveConversationId(id);
    setLoading(false);
  }

  // --------------------------------------------------
  // UI
  // --------------------------------------------------

  return (
    <div className="app-shell">
      <Sidebar
        conversations={conversations.map(
          (item) => item.conversation
        )}
        onNewConversation={handleNewConversation}
        collapsed={collapsed}
        onToggle={() =>
          setCollapsed((current) => !current)
        }
        onSelectConversation={handleSelectConversation}
        activeConversationId={activeConversationId}
      />

      <SearchWorkspace
        query={query}
        setQuery={setQuery}
        onSearch={handleSearch}
        messages={messages}
        loading={loading}
      />
    </div>
  );
}