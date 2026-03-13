import os
import re
from pathlib import Path
from importlib import resources
try:
    from notebooklm import __version__ as version
except ImportError:
    version = "unknown"

def get_skill_source_content() -> str:
    """Read the skill source file from package data."""
    try:
        # Python 3.9+ way to read package data (use / operator for path traversal)
        return (resources.files("notebooklm") / "data" / "SKILL.md").read_text(encoding="utf-8")
    except (FileNotFoundError, TypeError):
        return ""

def main():
    skill_dest_dir = Path.home() / ".gemini" / "antigravity" / "skills" / "notebooklm"
    skill_dest = skill_dest_dir / "SKILL.md"
    
    content = get_skill_source_content()
    if not content:
        print("Error: Skill source not found in package data.")
        return
        
    skill_dest_dir.mkdir(parents=True, exist_ok=True)
    
    # Just write the file
    with open(skill_dest, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"Installed NotebookLM skill for Antigravity to {skill_dest}")

if __name__ == "__main__":
    main()
