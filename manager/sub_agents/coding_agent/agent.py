from google.adk.agents.llm_agent import LlmAgent
from dotenv import load_dotenv
from .utils.instructions_loader import load_instructions_from_file
from .tools.github_tool import (
    get_github_user_info, list_github_repos, create_github_repo, create_github_issue, get_latest_commit,
    clone_github_repo, pull_latest_changes, push_local_changes, create_pull_request, update_github_file, delete_github_file,
    list_github_branches, create_github_branch, merge_github_branches, add_github_collaborator
)
from .tools.filesystem_tools import create_file, read_file, update_file, delete_file, list_dir, run_shell_command
from .tools.agent_management_tools import create_sub_agent


import os


load_dotenv(os.path.join(os.path.dirname(__file__), "../../../.env"))

coding_agent = LlmAgent(
    name="coding_agent",
    model="gemini-2.0-pro",
    description="Handles coding tasks and debugging using LLMs.",
    instruction=load_instructions_from_file("CODING_AGENT_INSTRUCTIONS.md"),
    sub_agents=[],
    tools=[
        get_github_user_info, list_github_repos, create_github_repo, create_github_issue, get_latest_commit,
        clone_github_repo, pull_latest_changes, push_local_changes, create_pull_request, update_github_file, delete_github_file,
        list_github_branches, create_github_branch, merge_github_branches, add_github_collaborator,
        create_file, read_file, update_file, delete_file, list_dir, run_shell_command, create_sub_agent
    ],
)

# --- Shared Session State Example for Sub-Agents ---
def handle_coding_task(task, session):
    """
    Example function for the coding_agent to demonstrate reading/writing shared session state.
    All sub-agents should follow this pattern to access shared memory.
    """
    # Read from shared session state
    last_user_request = session.state.get('last_user_request')
    # Log this agent's last task
    session.state['coding_agent_last_task'] = task
    # Optionally, append to a shared actions log
    session.state.setdefault('actions', []).append({
        'agent': 'coding_agent',
        'task': task
    })
    # Return something for demonstration
    return {
        'last_user_request': last_user_request,
        'coding_agent_last_task': task,
        'all_actions': session.state['actions']
    }

# Document for other sub-agents: Accept `session` as an argument, use session.state for shared memory.