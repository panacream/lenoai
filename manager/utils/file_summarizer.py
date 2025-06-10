import os

def summarize_file(file_path: str, max_lines: int = 60) -> str:
    """
    Returns a plain-text summary of a file by reading its first `max_lines` lines.
    Args:
        file_path (str): Path to the file to summarize.
        max_lines (int): Maximum number of lines to return from the file.
    Returns:
        str: The summary (first `max_lines` lines) of the file, or an error message if not found.
    """
    if not os.path.exists(file_path):
        return f"File not found: {file_path}"
    try:
        with open(file_path, encoding='utf-8') as f:
            lines = f.readlines()
        summary = ''.join(lines[:max_lines])
        if len(lines) > max_lines:
            summary += f"\n... (truncated, {len(lines)-max_lines} more lines)"
        return summary
    except Exception as e:
        return f"Error reading file: {e}"
