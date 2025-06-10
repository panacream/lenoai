import { useState, useEffect, useRef } from "react";
import { sendAgentMessage } from "../lib/agentApi";
import { isActionableTask } from "../config/actionableTasksConfig";

type ChatMessage = {
  role: "user" | "agent";
  content: string;
};

export type ActionLog = {
  id: string;
  task: string;
  agent: string;
  status: "pending" | "completed" | "failed";
  timestamp: string;
  duration?: string;
  output?: string;
};

const CHAT_STORAGE_KEY = "agent_chat_history";
const ACTION_LOG_STORAGE_KEY = "agent_action_logs";

function loadMessagesFromStorage(): ChatMessage[] {
  try {
    const stored = localStorage.getItem(CHAT_STORAGE_KEY);
    if (stored) {
      return JSON.parse(stored);
    }
  } catch (e) {
    // If JSON parsing fails, return empty array
    return [];
  }
  return [];
}

function loadActionLogsFromStorage(): ActionLog[] {
  try {
    const stored = localStorage.getItem(ACTION_LOG_STORAGE_KEY);
    if (stored) {
      return JSON.parse(stored);
    }
  } catch (e) {
    return [];
  }
  return [];
}

export function useAgentChat() {
  const [messages, setMessages] = useState<ChatMessage[]>(loadMessagesFromStorage());
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [actionLogs, setActionLogs] = useState<ActionLog[]>(loadActionLogsFromStorage());
  const isFirstRender = useRef(true);

  // Persist messages to localStorage whenever they change
  useEffect(() => {
    // Avoid saving on first render if storage already loaded
    if (isFirstRender.current) {
      isFirstRender.current = false;
      return;
    }
    localStorage.setItem(CHAT_STORAGE_KEY, JSON.stringify(messages));
  }, [messages]);

  // Persist action logs to localStorage whenever they change
  useEffect(() => {
    localStorage.setItem(ACTION_LOG_STORAGE_KEY, JSON.stringify(actionLogs));
  }, [actionLogs]);

  const clearMessages = () => {
    setMessages([]);
    localStorage.removeItem(CHAT_STORAGE_KEY);
  };

  const addActionLog = (log: Omit<ActionLog, "id" | "timestamp"> & { id?: string; timestamp?: string }) => {
    const fullLog: ActionLog = {
      id: log.id || `${Date.now()}-${Math.random().toString(36).substr(2, 5)}`,
      timestamp: log.timestamp || new Date().toISOString(),
      ...log,
    };
    setActionLogs((prev) => [fullLog, ...prev]);
  };

  const sendMessage = async (userMessage: string) => {
    setLoading(true);
    setError(null);
    try {
      const agentResponse = await sendAgentMessage(userMessage);
      const agentContent =
        typeof agentResponse === "string"
          ? agentResponse
          : agentResponse.reply ||
            agentResponse.response ||
            agentResponse.message ||
            JSON.stringify(agentResponse);
      setMessages((msgs) => [
        ...msgs,
        { role: "user", content: userMessage },
        { role: "agent", content: agentContent }
      ]);

      // Detect actionable task using custom matcher
      if (isActionableTask(agentContent)) {
        addActionLog({
          task: userMessage,
          agent: "Leno AI",
          status: "completed",
          output: agentContent
        });
      }
    } catch (err: unknown) {
      if (typeof err === "object" && err !== null && "message" in err) {
        setError((err as { message?: string }).message || "Unknown error");
      } else {
        setError("Unknown error");
      }
    } finally {
      setLoading(false);
    }
  };

  return { messages, sendMessage, loading, error, clearMessages, actionLogs, addActionLog };
}
