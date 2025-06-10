import os

def create_file(path: str, content: str):
    """Create a file at 'path' with the given content."""
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return {"status": "success", "message": f"Created file {path}"}
    except Exception as e:
        return {"status": "error", "error": str(e)}

def read_file(path: str):
    """Read the contents of a file at 'path'."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        return {"status": "success", "content": content}
    except Exception as e:
        return {"status": "error", "error": str(e)}

def update_file(path: str, content: str):
    """Overwrite the contents of a file at 'path'."""
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return {"status": "success", "message": f"Updated file {path}"}
    except Exception as e:
        return {"status": "error", "error": str(e)}

def delete_file(path: str):
    """Delete the file at 'path'."""
    try:
        os.remove(path)
        return {"status": "success", "message": f"Deleted file {path}"}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def delete_path(path: str):
    """
    Delete a file or directory at 'path'. If it's a directory, delete recursively.
    """
    import os
    import shutil
    try:
        if os.path.isfile(path):
            os.remove(path)
            return {"status": "success", "message": f"Deleted file {path}"}
        elif os.path.isdir(path):
            shutil.rmtree(path)
            return {"status": "success", "message": f"Deleted directory {path}"}
        else:
            return {"status": "error", "error": f"Path not found: {path}"}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def list_dir(path: str):
    """List files and directories at 'path'."""
    try:
        items = os.listdir(path)
        return {"status": "success", "items": items}
    except Exception as e:
        return {"status": "error", "error": str(e)}

def run_shell_command(command: str, cwd: str):
    """Run a shell command in the specified directory."""
    import subprocess
    try:
        result = subprocess.run(command, cwd=cwd, shell=True, capture_output=True, text=True)
        return {
            "status": "success" if result.returncode == 0 else "error",
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}
