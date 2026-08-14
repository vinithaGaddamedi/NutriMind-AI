import React, { useState, useRef, useEffect } from 'react';
import { sendChatMessage } from '../api/client';

const DEFAULT_WELCOME_MESSAGE = {
  sender: 'ai',
  text: '👋 Hello! I am your NutriMind AI Assistant. Ask me anything about weekly meal planning, nutritional macros, pantry management, or smart grocery shopping!',
  timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
};

export default function ChatWidget({ userId = null }) {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([DEFAULT_WELCOME_MESSAGE]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [conversationId, setConversationId] = useState(null);

  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    if (isOpen) {
      scrollToBottom();
    }
  }, [messages, isOpen]);

  const handleSend = async (e) => {
    e.preventDefault();
    const trimmed = input.trim();
    if (!trimmed || loading) return;

    const userMsg = {
      sender: 'user',
      text: trimmed,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setLoading(true);
    setError(null);

    try {
      const data = await sendChatMessage(trimmed, conversationId, { user_id: userId });
      if (data.conversation_id) {
        setConversationId(data.conversation_id);
      }

      const aiMsg = {
        sender: 'ai',
        text: data.response,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        model: data.model
      };

      setMessages(prev => [...prev, aiMsg]);
    } catch (err) {
      console.error('Failed to send chat message:', err);
      setError('Failed to reach NutriMind AI backend. Please verify backend service status.');
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setMessages([DEFAULT_WELCOME_MESSAGE]);
    setConversationId(null);
    setError(null);
  };

  return (
    <div className="chat-widget-container">
      {/* Floating Toggle Button */}
      {!isOpen && (
        <button
          className="chat-toggle-btn btn btn-primary"
          onClick={() => setIsOpen(true)}
          aria-label="Open NutriMind AI Assistant Chat"
          id="nutrimind-chat-toggle"
        >
          <span className="chat-icon">🤖</span> NutriMind AI
        </button>
      )}

      {/* Expandable Glassmorphism Chat Panel */}
      {isOpen && (
        <div className="chat-panel glass-panel animate-fade-up" role="region" aria-label="NutriMind AI Chat Window">
          {/* Header */}
          <div className="chat-header">
            <div className="chat-title">
              <span className="chat-avatar">🥗</span>
              <div>
                <h4>NutriMind AI Assistant</h4>
                <small style={{ opacity: 0.8, fontSize: '0.75rem' }}>AI Nutrition Engine</small>
              </div>
            </div>
            <div className="chat-header-actions">
              <button
                className="btn-text-action"
                onClick={handleClear}
                title="Clear Conversation"
                aria-label="Clear Conversation"
                id="nutrimind-chat-clear"
              >
                Clear
              </button>
              <button
                className="btn-close"
                onClick={() => setIsOpen(false)}
                aria-label="Close Chat Window"
                id="nutrimind-chat-close"
              >
                ✕
              </button>
            </div>
          </div>

          {/* Messages Container */}
          <div className="chat-messages" role="log" aria-live="polite">
            {messages.map((msg, index) => (
              <div key={index} className={`chat-message ${msg.sender}`}>
                <div className="message-content">
                  <p>{msg.text}</p>
                  <span className="message-time">{msg.timestamp}</span>
                </div>
              </div>
            ))}

            {loading && (
              <div className="chat-message ai loading-bubble">
                <div className="typing-indicator">
                  <span></span><span></span><span></span>
                </div>
              </div>
            )}

            {error && (
              <div className="chat-error-banner" role="alert">
                ⚠️ {error}
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input Form */}
          <form className="chat-input-form" onSubmit={handleSend}>
            <input
              type="text"
              className="chat-input"
              placeholder="Ask about meal plans, nutrition, pantry..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              aria-label="Type your message"
              disabled={loading}
              id="nutrimind-chat-input"
            />
            <button
              type="submit"
              className="btn btn-primary chat-send-btn"
              disabled={loading || !input.trim()}
              aria-label="Send Message"
              id="nutrimind-chat-send"
            >
              Send
            </button>
          </form>
        </div>
      )}
    </div>
  );
}
