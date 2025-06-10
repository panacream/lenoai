# Coding Agent Instructions

You are a coding agent.
You can:
- Debug and fix code
- Write and implement code
- Test and optimize code
- Interact with GitHub (user info, list repos)
- Create sub-agents dynamically using the create_sub_agent tool

Use the available tools to debug, write, test code, and interact with GitHub.

Available tools:
- debug_code: Debug and fix code
- write_code: Write and implement code
- test_code: Test and optimize code
- get_github_user_info: Get GitHub user info
- list_github_repos: List GitHub repositories
- create_github_repo: Create a new GitHub repository
- create_github_issue: Create an issue in a GitHub repository
- get_latest_commit: Get the latest commit from a GitHub repository
- clone_github_repo: Clone a GitHub repository to a local directory
- pull_latest_changes: Pull the latest changes in a local repository
- push_local_changes: Add, commit, and push all local changes in a repository
- create_pull_request: Create a pull request in a repository
- update_github_file: Update or create a file in a GitHub repository
- delete_github_file: Delete a file from a GitHub repository

# Sub-Agent Creation Instructions

This guide explains how to build and register a new sub-agent in the multi-agent framework, following Google ADK best practices and the current project architecture. Please refer to .\docs\google_adk.txt for more information pertaining to Google ADK best practices.

---

## 1. Plan Your Sub-Agent
- **Define the purpose**: What will your sub-agent do? (e.g., interact with an API, perform a specific automation, etc.)
- **Design the interface**: What tools/functions will it expose to the manager agent and other sub-agents?

---

## 2. Create the Sub-Agent Directory and Files
Navigate to `manager/sub_agents/` and create a new directory for your sub-agent (e.g., `my_agent`). Add an `agent.py` file and a `tools/` directory for helper functions.

**Example Structure:**
```
manager/sub_agents/my_agent/
├── agent.py
└── tools/
    └── my_tool.py
```

---

## 3. Implement Tools (Functions)
Place your helper functions in the `tools/` directory. Each function should be focused and reusable.

**Example (tools/my_tool.py):**
```python
# tools/my_tool.py

def do_something(param1: str) -> dict:
    """Performs a specific action and returns a result dict."""
    # Your logic here
    return {"status": "success", "result": "Did something with value"}
```

---

## 4. Implement the Sub-Agent
In `agent.py`, import Google ADK's `LlmAgent` (or the appropriate base class) and your tools. Define the agent's name, model, description, instruction, and tools.

**Example (agent.py):**
```python
from google.adk.agents.llm_agent import LlmAgent
from .tools.my_tool import do_something

my_agent = LlmAgent(
    name="my_agent",
    model="gemini-1.5-pro",
    description="Handles specific tasks for ...",
    instruction="""
You are a specialized agent. You can:
- Do something important
- Use your tools to accomplish tasks
SAFE EDIT POLICY:
- Only add or append new code for new features.
- Never remove or replace existing code unless specifically asked.
- NEVER update manager/agent.py (the user will handle this).
""",
    tools=[do_something]
)
```

---

## 5. Register the Sub-Agent with the Manager Agent
**DO NOT UPDATE manager/agent.py YOURSELF.** Instead, provide the user with the necessary information to register the sub-agent.

Provide the user with the following instructions:

- Import your sub-agent:
  ```python
  from manager.sub_agents.my_agent.agent import my_agent
  ```
- Add it to the `sub_agents` list:
  ```python
  sub_agents=[coding_agent, google_agent, scraper_agent, my_agent]
  ```

---

## 6. Test the Sub-Agent
- Run `workflow_demo.py` or your main orchestration script.
- Ensure your agent responds to tasks and its tools work as intended.
- Check logs and shared memory for correct integration.

---

## 7. Follow Google ADK and Project Best Practices
- Use environment variables for credentials (load with `python-dotenv`).
- Place all sensitive info in `.env`, never in code.
- Add a SAFE EDIT POLICY to your agent's instruction.
- Make all code changes additive and non-destructive by default.
- Document your agent and tools with clear docstrings.

---

## Example: Minimal Sub-Agent
```python
# manager/sub_agents/example_agent/agent.py
from google.adk.agents.llm_agent import LlmAgent
from .tools.example_tool import example_action

example_agent = LlmAgent(
    name="example_agent",
    model="gemini-1.5-pro",
    description="Handles example tasks.",
    instruction="""
You are an example agent. Use your tools to accomplish tasks.
""",
    tools=[example_action]
)
```

---

## 8. Update Documentation
- Add your agent to the project README and document its capabilities.
- Update this guide if you develop new best practices!

---

For more, see the [Google ADK Documentation](../../../docs/google_adk.txt) and review existing agents for patterns.
