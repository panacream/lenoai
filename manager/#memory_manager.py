# === DEPRECATED! === //
# All memory and logging is now handled by Google ADK session.state and event logging.
# This file is no longer used.
def add_memory(event_type, content, metadata=None):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "event_type": event_type,
        "content": content,
        "metadata": metadata or {}
    }
    with open(MEMORY_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")

def get_memories(event_type=None, query=None):
    memories = []
    if not os.path.exists(MEMORY_FILE):
        return memories
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        for line in f:
            entry = json.loads(line)
            if event_type and entry["event_type"] != event_type:
                continue
            if query and query.lower() not in entry["content"].lower():
                continue
            memories.append(entry)
    return memories

def has_read_doc(doc_path):
    return any(
        m for m in get_memories(event_type="doc_read")
        if m["metadata"].get("doc_path") == doc_path
    )

def summarize_and_store_doc(doc_path):
    if has_read_doc(doc_path):
        return
    with open(doc_path, "r", encoding="utf-8") as f:
        content = f.read()
    # For now, just store first 1000 chars as summary
    summary = content[:1000]
    add_memory("doc_read", summary, {"doc_path": doc_path})
