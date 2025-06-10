# Test Workflow: Creating New Sub-Agents with the Coding Agent

This test workflow demonstrates how to use the coding agent to create a new sub-agent, following project and Google ADK best practices.

---

## 1. Define the Sub-Agent
- **Purpose:** (e.g., Integrate with a new API, automate a workflow)
- **Tools:** List the functions/tools the agent should provide.

## 2. Scaffold the Sub-Agent Structure
- Request the coding agent to:
    - Create a folder: `manager/sub_agents/example_agent/`
    - Add `agent.py` and a `tools/` directory inside it.

## 3. Implement Tools
- For each tool, ask the coding agent to create a Python function in `tools/` (with docstrings and clear parameters).
- Example:
    - `tools/example_tool.py` with `def example_action(...)`.

## 4. Implement the Agent Class
- Instruct the coding agent to:
    - Import `LlmAgent` from Google ADK.
    - Import all tools.
    - Define the agent in `agent.py` with name, model, description, instruction (with SAFE EDIT POLICY), and tools list.

## 5. Review and Refine
- Review generated code for accuracy and adherence to SAFE EDIT POLICY.
- Ask the coding agent to make any needed refinements.

## 6. Testing
- Request the coding agent to provide or update test scripts for the new sub-agent.
- Example: `test_example_agent.py` with tests for each tool and agent response.
- Run tests to confirm correct behavior.

## 7. Registration (Manual Step)
- The user (not the coding agent) must update `manager/agent.py` to register the new sub-agent.
- The coding agent should output the required import and registration code for you to copy.

## 8. Documentation
- Ask the coding agent to update or create documentation for the new sub-agent and its tools.

## 9. Final Review
- Ensure all code is modular, documented, and follows Google ADK and project best practices.

---

## Example Test Case
```python
# test_example_agent.py
from manager.sub_agents.example_agent.agent import example_agent

def test_example_action():
    result = example_agent.tools[0]("test input")
    assert result["status"] == "success"
    assert "Did something with" in result["result"]
```

---

By following this workflow and running the tests, you can ensure every new sub-agent is created, tested, and documented to project standards.
