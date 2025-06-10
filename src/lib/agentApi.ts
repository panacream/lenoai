const API_BASE = import.meta.env.VITE_AGENT_API_URL || "http://localhost:3001/api";

export async function sendAgentMessage(message: string, context: any = {}) {
  const response = await fetch(`${API_BASE}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, ...context }),
  });
  if (!response.ok) throw new Error("Agent API error");
  return response.json();
}
