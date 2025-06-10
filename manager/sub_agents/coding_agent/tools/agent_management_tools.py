import os

def create_sub_agent(agent_name: str, agent_spec: dict) -> dict:
    """
    Creates a new sub-agent directory with the required agent.py and supporting files.

    Args:
        agent_name (str): The name of the new sub-agent (e.g., 'greeting_agent').
        agent_spec (dict): Specification for the agent, including:
            - description (str)
            - greeting_message (str)
            - name_prompt (str)
            - response_template (str)
            - (any other custom logic or files)

    Returns:
        dict: {"status": "success", "message": "..."} or {"status": "error", "message": "..."}
    """
    try:
        base_dir = os.path.join(os.path.dirname(__file__), '..', agent_name)
        os.makedirs(base_dir, exist_ok=True)

        # Write agent.py
        agent_py = f"""from google.adk.agents.llm_agent import LlmAgent

greeting_message = {repr(agent_spec.get('greeting_message', 'Hello, what is your name?'))}
response_template = {repr(agent_spec.get('response_template', 'Nice to meet you {{name}}.'))}

def handle_greeting(context):
    if 'name' in context:
        return response_template.format(name=context['name'])
    return greeting_message

greeting_agent = LlmAgent(
    name="{agent_name}",
    model="gemini-1.5-pro",
    description={repr(agent_spec.get('description', 'A simple greeting agent.'))},
    instruction=\"\"\"This agent greets the user and asks for their name. When the user provides their name, it responds with a personalized message.\"\"\",
    tools=[handle_greeting]
)
"""
        with open(os.path.join(base_dir, "agent.py"), "w", encoding="utf-8") as f:
            f.write(agent_py)

        # Write README
        with open(os.path.join(base_dir, "README.md"), "w", encoding="utf-8") as f:
            f.write(f"# {agent_name}\n\n{agent_spec.get('description', 'A simple greeting agent.')}\n")

        return {"status": "success", "message": f"Sub-agent '{agent_name}' created successfully."}
    except Exception as e:
        return {"status": "error", "message": f"Failed to create sub-agent: {e}"}