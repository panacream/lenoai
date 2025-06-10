import os

def load_instructions_from_file(filename: str) -> str:
    """
    Loads the full text of the instructions file from the docs folder within the coding_agent directory.
    Args:
        filename (str): The name of the file to load (e.g., "sub_agent_creation_instructions.md").
    Returns:
        str: The contents of the file as a string.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    docs_path = os.path.join(base_dir, "docs", filename)
    with open(docs_path, "r", encoding="utf-8") as f:
        return f.read()
