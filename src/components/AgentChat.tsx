import { useState, useRef, useEffect } from "react";
import type { useAgentChat as useAgentChatType } from "../hooks/useAgentChat";

interface AgentChatProps {
  agentChat: ReturnType<typeof useAgentChatType>;
}

const AgentChat: React.FC<AgentChatProps> = ({ agentChat }) => {
  const { messages, sendMessage, loading, error, clearMessages } = agentChat;
  const [input, setInput] = useState("");
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  // Scroll to bottom on new messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });

  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;
    await sendMessage(input);
    setInput("");
  };

  const handleClear = () => {
    clearMessages();
  };

  return (
    <div className="max-w-xl mx-auto mt-8 p-4 bg-white rounded shadow">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-2xl font-bold text-blue-600">Leno AI Chat</h2>
        <button
          className="bg-gray-200 text-gray-700 px-3 py-1 rounded hover:bg-red-100 hover:text-red-600 border border-gray-300 text-sm"
          onClick={handleClear}
          type="button"
        >
          Clear Chat
        </button>
      </div>
      <div className="h-64 overflow-y-auto mb-4 border rounded p-2 bg-gray-50">
        {messages.length === 0 && <div className="text-gray-400">Start the conversation...</div>}
        {messages.map((msg, idx) => (
          <div key={idx} className={`mb-2 text-${msg.role === "user" ? "right" : "left"}`}> 
            <span className={msg.role === "user" ? "text-blue-700 font-semibold" : "text-green-700 font-semibold"}>
              {msg.role === "user" ? "You" : "Leno AI"}:
            </span> {msg.content}
          </div>
        ))}
        {loading && <div className="text-gray-500">Agent is typing...</div>}
        <div ref={messagesEndRef} />
      </div>
      <form onSubmit={handleSubmit} className="flex gap-2">
        <input
          type="text"
          className="flex-1 border rounded px-3 py-2 focus:outline-none focus:ring"
          placeholder="Type your message..."
          value={input}
          onChange={e => setInput(e.target.value)}
          disabled={loading}
        />
        <button
          type="submit"
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 disabled:opacity-50"
          disabled={loading || !input.trim()}
        >
          Send
        </button>
      </form>
      {error && <div className="text-red-600 mt-2">Error: {error}</div>}
    </div>
  );
};

export default AgentChat;
