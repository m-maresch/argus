import logging

from pathlib import Path


def _project_root():
    """Traverse upward from the current file until the project root is found."""
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / "prompt.md").exists():
            return parent
    return current.parent


def load_user_prompt():
    project_root = _project_root()
    prompt_path = project_root / "prompt.md"
    logging.info(f"Loading prompt from {prompt_path}")
    user_prompt = prompt_path.read_text(encoding="utf-8").strip()
    return user_prompt
