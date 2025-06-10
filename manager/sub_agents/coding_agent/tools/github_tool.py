from github import Github

def get_github_user_info(username: str):
    """
    Fetch GitHub user info. If username is an empty string, fetches the authenticated user.
    """
    import os
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    g = Github(GITHUB_TOKEN)
    try:
        user = g.get_user(username) if username else g.get_user()
        return {
            "status": "success",
            "login": user.login,
            "public_repos": user.public_repos,
            "followers": user.followers,
            "bio": user.bio,
            "url": user.html_url,
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}


def clone_github_repo(repo_url: str, local_path: str):
    """
    Clone a GitHub repository to a local directory.
    Supports both HTTPS (with token injection) and SSH URLs.

    If the target directory exists, it will be deleted automatically (with a warning in the response).
    Returns detailed stdout and stderr for debugging.
    """
    import subprocess
    import os
    import shutil

    warning = None

    # Check if the directory exists
    if os.path.exists(local_path):
        try:
            shutil.rmtree(local_path)
            warning = f"WARNING: The directory '{local_path}' already existed and was deleted before cloning."
        except Exception as e:
            return {
                "status": "error",
                "error": f"Target directory '{local_path}' exists and could not be deleted: {str(e)}",
                "warning": warning
            }

    # Inject token for HTTPS URLs if not already present
    if repo_url.startswith("https://") and "@" not in repo_url:
        token = os.getenv("GITHUB_TOKEN")
        if token:
            repo_url = repo_url.replace("https://", f"https://{token}@")

    try:
        result = subprocess.run(["git", "clone", repo_url, local_path], capture_output=True, text=True)
        if result.returncode == 0:
            return {
                "status": "success",
                "message": f"Cloned to {local_path}",
                "stdout": result.stdout,
                "stderr": result.stderr,
                "warning": warning
            }
        else:
            return {
                "status": "error",
                "error": result.stderr,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "warning": warning
            }
    except Exception as e:
        return {"status": "error", "error": str(e), "warning": warning}


def pull_latest_changes(local_path: str):
    """
    Pull the latest changes in the current branch of a local repo.
    """
    import subprocess
    try:
        result = subprocess.run(["git", "-C", local_path, "pull"], capture_output=True, text=True)
        if result.returncode == 0:
            return {"status": "success", "message": result.stdout}
        else:
            return {"status": "error", "error": result.stderr}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def push_local_changes(local_path: str, commit_message: str):
    """
    Add, commit, and push all local changes in a repo. Pass a commit message string.
    """
    import subprocess
    try:
        subprocess.run(["git", "-C", local_path, "add", "."], check=True)
        subprocess.run(["git", "-C", local_path, "commit", "-m", commit_message], check=True)
        result = subprocess.run(["git", "-C", local_path, "push"], capture_output=True, text=True)
        if result.returncode == 0:
            return {"status": "success", "message": result.stdout}
        else:
            return {"status": "error", "error": result.stderr}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def create_pull_request(repo_name: str, title: str, body: str, head: str, base: str):
    """
    Create a pull request in a repo you own. Specify all arguments as strings. (e.g., base="main")
    """
    import os
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    g = Github(GITHUB_TOKEN)
    try:
        user = g.get_user()
        repo = user.get_repo(repo_name)
        pr = repo.create_pull(title=title, body=body, head=head, base=base)
        return {"status": "success", "pr_url": pr.html_url}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def update_github_file(repo_name: str, file_path: str, new_content: str, commit_message: str):
    """
    Update or create a file in a GitHub repo. Pass commit_message as a string.
    """
    import os
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    g = Github(GITHUB_TOKEN)
    try:
        user = g.get_user()
        repo = user.get_repo(repo_name)
        contents = repo.get_contents(file_path)
        repo.update_file(contents.path, commit_message, new_content, contents.sha)
        return {"status": "success", "message": f"Updated {file_path}"}
    except Exception as e:
        # Try to create if not exist
        try:
            repo.create_file(file_path, commit_message, new_content)
            return {"status": "success", "message": f"Created {file_path}"}
        except Exception as e2:
            return {"status": "error", "error": str(e2)}


def add_folder_to_github_repo(repo_name: str, folder_path: str, commit_message: str):
    """
    Add a folder to a GitHub repo by creating a .gitkeep file in it. Pass commit_message as a string.
    folder_path should be the path to the folder (e.g., 'test/') and will create 'test/.gitkeep'.
    """
    import os
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    g = Github(GITHUB_TOKEN)
    try:
        user = g.get_user()
        repo = user.get_repo(repo_name)
        # Ensure folder_path ends with a slash
        if not folder_path.endswith('/'):
            folder_path += '/'
        file_path = folder_path + '.gitkeep'
        content = ''  # Empty file
        try:
            # Try to get the file (should not exist)
            repo.get_contents(file_path)
            return {"status": "success", "message": f"Folder already exists with .gitkeep at {file_path}"}
        except Exception:
            # File does not exist, so create it
            repo.create_file(file_path, commit_message, content)
            return {"status": "success", "message": f"Created folder {folder_path} in repo {repo_name}"}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def delete_github_file(repo_name: str, file_path: str, commit_message: str):
    """
    Delete a file from a GitHub repo. Pass commit_message as a string.
    """
    import os
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    g = Github(GITHUB_TOKEN)
    try:
        user = g.get_user()
        repo = user.get_repo(repo_name)
        contents = repo.get_contents(file_path)
        repo.delete_file(contents.path, commit_message, contents.sha)
        return {"status": "success", "message": f"Deleted {file_path}"}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def list_github_branches(repo_name: str):
    """
    List all branches in a GitHub repo.
    """
    g = Github(GITHUB_TOKEN)
    try:
        user = g.get_user()
        repo = user.get_repo(repo_name)
        branches = [branch.name for branch in repo.get_branches()]
        return {"status": "success", "branches": branches}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def create_github_branch(repo_name: str, new_branch: str, source_branch: str):
    """
    Create a new branch from source_branch in a repo you own. Specify all arguments as strings.
    """
    import os
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    g = Github(GITHUB_TOKEN)
    try:
        user = g.get_user()
        repo = user.get_repo(repo_name)
        sb = repo.get_branch(source_branch)
        repo.create_git_ref(ref=f"refs/heads/{new_branch}", sha=sb.commit.sha)
        return {"status": "success", "message": f"Created branch {new_branch} from {source_branch}"}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def merge_github_branches(repo_name: str, base: str, head: str):
    """
    Merge head branch into base branch in a repo you own. Specify all arguments as strings.
    """
    import os
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    g = Github(GITHUB_TOKEN)
    try:
        user = g.get_user()
        repo = user.get_repo(repo_name)
        merge = repo.merge(base, head)
        return {"status": "success", "message": f"Merged {head} into {base}", "merge_commit_sha": merge.sha}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def add_github_collaborator(repo_name: str, collaborator: str, permission: str):
    """
    Add a collaborator to a GitHub repo. Specify permission as a string (e.g., "push", "pull", "admin").
    """
    import os
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    g = Github(GITHUB_TOKEN)
    try:
        user = g.get_user()
        repo = user.get_repo(repo_name)
        repo.add_to_collaborators(collaborator, permission)
        return {"status": "success", "message": f"Added {collaborator} as collaborator with {permission} permission."}
    except Exception as e:
        return {"status": "error", "error": str(e)}

def list_github_repos(username: str):
    """
    List public repos for a user. If username is an empty string, lists your own repos.
    """
    import os
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    g = Github(GITHUB_TOKEN)
    try:
        user = g.get_user(username) if username else g.get_user()
        repos = [{"name": repo.name, "url": repo.html_url} for repo in user.get_repos()]
        return {"status": "success", "repos": repos}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def create_github_repo(repo_name: str, private: bool, description: str):
    """
    Create a new repository under your authenticated account. Set description to empty string for no description. Set private to True or False explicitly.
    """
    import os
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    g = Github(GITHUB_TOKEN)
    try:
        user = g.get_user()
        repo = user.create_repo(name=repo_name, private=private, description=description)
        return {"status": "success", "repo_url": repo.html_url}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def create_github_issue(repo_name: str, title: str, body: str):
    """
    Create an issue in a repository owned by the authenticated user. Set body to empty string for no description.
    """
    import os
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    g = Github(GITHUB_TOKEN)
    try:
        user = g.get_user()
        repo = user.get_repo(repo_name)
        issue = repo.create_issue(title=title, body=body)
        return {"status": "success", "issue_url": issue.html_url}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def get_latest_commit(repo_name: str):
    """
    Get the latest commit on the default branch for a repo owned by the authenticated user.
    """
    import os
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    g = Github(GITHUB_TOKEN)
    try:
        user = g.get_user()
        repo = user.get_repo(repo_name)
        commit = repo.get_commits()[0]
        return {"status": "success", "sha": commit.sha, "message": commit.commit.message, "url": commit.html_url}
    except Exception as e:
        return {"status": "error", "error": str(e)}
