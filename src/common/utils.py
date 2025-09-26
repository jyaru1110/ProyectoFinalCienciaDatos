from pathlib import Path


# Esta función se generó usando Claude Sonnet 4
def find_project_root(start_path=None):
    """Find the project root by looking for pyproject.toml"""
    current_path = Path(__file__).resolve() if start_path is None else Path(start_path).resolve()

    project_root = None
    for parent in current_path.parents:
        if (parent / "pyproject.toml").exists():
            project_root = parent
            break

    if project_root is None:
        # Fallback to current file's directory if pyproject.toml not found
        project_root = current_path.parent

    return project_root
