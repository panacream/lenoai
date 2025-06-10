"""
Test Workflow: Creating a New Sub-Agent Using the Coding Agent
This script demonstrates, end-to-end, how to use the coding agent to scaffold, implement, and test a new sub-agent in the framework, following Google ADK best practices.
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))
from dotenv import load_dotenv
from google.adk.sessions import InMemorySessionService
from manager.sub_agents.coding_agent.tools.github_tool import create_github_repo
from manager.sub_agents.coding_agent.tools.filesystem_tools import create_file, list_dir

# 1. Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '../../../.env'))

# 2. Create a session service and a new session (for agent context, if needed)
session_service = InMemorySessionService()
session = session_service.create_session(
    app_name="agent4_app",
    user_id="user_demo",
    session_id="test_sub_agent_workflow"
)

# 3. Define sub-agent parameters
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))
tag = "demo_agent"
sub_agent_dir = f"manager/sub_agents/{tag}/"
tools_dir = os.path.join(sub_agent_dir, "tools")
agent_py = os.path.join(sub_agent_dir, "agent.py")
tool_py = os.path.join(tools_dir, "demo_tool.py")

# 4. Scaffold the sub-agent folder and files using the coding agent's tools
os.makedirs(tools_dir, exist_ok=True)
create_file(agent_py, "# Placeholder for agent definition\n")
create_file(tool_py, """def demo_action(param: str) -> dict:\n    \"\"\"Demo tool for the new sub-agent.\"\"\"\n    return {\"status\": \"success\", \"result\": f'Demo action with {param}'}\n""")

# 5. Implement the agent class (simulate what the coding agent would generate)
agent_code = f"""
from google.adk.agents.llm_agent import LlmAgent
from .tools.demo_tool import demo_action

demo_agent = LlmAgent(
    name=\"demo_agent\",
    model=\"gemini-1.5-pro\",
    description=\"Demo sub-agent created by workflow.\",
    instruction=\"\"\"
You are a demo agent. Use your tools to perform demo actions.\nSAFE EDIT POLICY:\n- Only add or append new code for new features.\n- Never remove or replace existing code unless specifically asked.\n- NEVER update manager/agent.py (the user will handle this).\n\"\"\",
    tools=[demo_action]
)
"""
with open(agent_py, "w", encoding="utf-8") as f:
    f.write(agent_code)

# 6. List the new sub-agent's files to verify creation
print("Sub-agent directory contents:", list_dir(sub_agent_dir))
print("Tools directory contents:", list_dir(tools_dir))

# 7. (Optional) Create a test repo for the new agent (simulate integration)
repo_name = f"demo-agent-repo-{tag}"
github_result = create_github_repo(repo_name, private=True, description="Demo repo for new sub-agent.")
print("GitHub Repo Creation Result:", github_result)

# 8. Output instructions for user to register the agent
print("\n*** MANUAL STEP REQUIRED ***")
print(f"To complete registration, add the following to manager/agent.py:\nfrom manager.sub_agents.{tag}.agent import demo_agent\nsub_agents.append(demo_agent)")
