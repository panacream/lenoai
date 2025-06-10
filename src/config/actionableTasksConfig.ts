// Configurable keywords and matcher for actionable tasks

export const ACTIONABLE_TASK_KEYWORDS = [
  // Add or remove keywords/phrases as needed
  "email sent",
  "added to google sheet",
  "scraped",
  "posted to linkedin",
  "token transferred",
  "minted",
  "burned",
  "created",
  "updated",
  "deleted"
];

/**
 * Optionally provide a custom matcher function for advanced detection.
 * Return true if the agent response/output is considered actionable.
 */
export function isActionableTask(agentContent: string): boolean {
  const lowerContent = agentContent.toLowerCase();
  return ACTIONABLE_TASK_KEYWORDS.some((kw) => lowerContent.includes(kw));
}
