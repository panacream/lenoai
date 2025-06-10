import os

def load_instructions_from_file(filename: str) -> str:
    """
    Loads the full text of the instructions file from the docs folder in the google agent directory.
    Args:
        filename (str): Name of the markdown instructions file (e.g., 'GOOGLE_AGENT_INSTRUCTIONS.md')
    Returns:
        str: Contents of the instruction file as a string.
    """
    docs_dir = os.path.join(os.path.dirname(__file__), '..', 'docs')
    path = os.path.join(docs_dir, filename)
    with open(path, encoding='utf-8') as f:
        return f.read()
