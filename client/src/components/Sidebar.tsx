
import {
  BrainCircuit,
  Plus,
  Search,
  Clock3,
  Settings,
  PanelLeftClose,
  PanelLeftOpen,
} from "lucide-react";
import type { Conversation } from "../types/search";

interface SidebarProps {
  conversations: Conversation[];
  onNewConversation: () => void;
  collapsed: boolean;
  onToggle: () => void;
  onSelectConversation: (id: string) => void;
  activeConversationId: string | null;
}

export default function Sidebar({
  conversations,
  onNewConversation,
  collapsed,
  onToggle,
  onSelectConversation,
  activeConversationId,
}: SidebarProps) {
  return (
    <aside className={`sidebar ${collapsed ? "sidebar-collapsed" : ""}`}>
      <div className="sidebar-top">
        <div className="brand">
          <div className="brand-icon">
            <BrainCircuit size={21} />
          </div>

          {!collapsed && (
            <div className="brand-text">
              <span className="brand-name">CogniVault</span>
              <span className="brand-subtitle">Knowledge intelligence</span>
            </div>
          )}
        </div>

        <button
          className="icon-button sidebar-toggle"
          onClick={onToggle}
          title={collapsed ? "Expand sidebar" : "Collapse sidebar"}
        >
          {collapsed ? (
            <PanelLeftOpen size={18} />
          ) : (
            <PanelLeftClose size={18} />
          )}
        </button>
      </div>

      <button
        className="new-chat-button"
        onClick={onNewConversation}
        title="New conversation"
      >
        <Plus size={18} />
        {!collapsed && <span>New conversation</span>}
      </button>

      <nav className="sidebar-nav">
        <div className="nav-item nav-item-active">
          <Search size={18} />
          {!collapsed && <span>Knowledge search</span>}
        </div>
      </nav>

      {!collapsed && (
        <div className="history-section">
          <div className="section-label">
            <Clock3 size={14} />
            <span>RECENT SEARCHES</span>
          </div>

          <div className="conversation-list">
            {conversations.length === 0 ? (
              <p className="empty-history">Your searches will appear here.</p>
            ) : (
              conversations.map((conversation) => (
                <button
                  key={conversation.id}
                  className={`conversation-item ${
                    activeConversationId === conversation.id
                      ? "conversation-active"
                      : ""
                  }`}
                  onClick={() => onSelectConversation(conversation.id)}
                  title={conversation.title}
                >
                  <span className="conversation-dot" />
                  <span className="conversation-title">
                    {conversation.title}
                  </span>
                </button>
              ))
            )}
          </div>
        </div>
      )}

      <div className="sidebar-bottom">
        <button className="sidebar-bottom-item" title="Settings">
          <Settings size={18} />
          {!collapsed && <span>Settings</span>}
        </button>

        {!collapsed && (
          <div className="sidebar-footer">
            <div className="footer-avatar">CV</div>
            <div className="footer-info">
              <span className="footer-name">CogniVault</span>
              <span className="footer-status">
                <span className="status-dot" />
                Knowledge system
              </span>
            </div>
          </div>
        )}
      </div>
    </aside>
  );
}
