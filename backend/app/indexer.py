import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any, Dict, Iterable, List

from app.config import REPOS_DIR
from app.embeddings import chunk_text, embedder, file_hash
from app.vector_store import vector_store


def get_language_for_path(path: str) -> str:
    suffix = Path(path).suffix.lower()
    return {
        ".py": "python",
        ".js": "javascript",
        ".ts": "typescript",
        ".tsx": "typescript",
        ".go": "go",
        ".rs": "rust",
        ".java": "java",
        ".cs": "csharp",
        ".md": "markdown",
        ".yml": "yaml",
        ".yaml": "yaml",
        ".json": "json",
        ".toml": "toml",
        ".sh": "bash",
    }.get(suffix, "text")


def should_index(path: str) -> bool:
    excluded = {".git", "node_modules", "dist", "build", "venv", "__pycache__", ".venv", ".next", "coverage"}
    if any(part in excluded for part in Path(path).parts):
        return False
    suffix = Path(path).suffix.lower()
    allowed = {".py", ".js", ".ts", ".tsx", ".go", ".rs", ".java", ".md", ".json", ".yml", ".yaml", ".toml", ".sh"}
    return suffix in allowed


def index_repo(repo_path: str, repo_name: str = "demo") -> Dict[str, Any]:
    repo_root = Path(repo_path)
    if not repo_root.exists():
        raise FileNotFoundError(f"Repository path does not exist: {repo_path}")

    points: List[Dict[str, Any]] = []
    indexed = 0

    for file_path in repo_root.rglob("*"):
        if not file_path.is_file() or not should_index(str(file_path)):
            continue
        try:
            text = file_path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        if not text.strip():
            continue
        for idx, chunk in enumerate(chunk_text(text)):
            vector = embedder.embed(chunk)
            points.append({
                "vector": vector,
                "payload": {
                    "repo": repo_name,
                    "path": str(file_path.relative_to(repo_root)),
                    "language": get_language_for_path(str(file_path)),
                    "chunk_index": idx,
                    "sha": file_hash(str(file_path)),
                    "content": chunk[:4000],
                },
            })
            indexed += 1

    vector_store.upsert_points(points)
    return {"repo": repo_name, "indexed": indexed, "points": len(points)}


def clone_repo(repo_url: str, repo_name: str | None = None) -> str:
    target_dir = REPOS_DIR / (repo_name or repo_url.rstrip("/").split("/")[-1])
    if target_dir.exists():
        shutil.rmtree(target_dir)
    subprocess.run(["git", "clone", "--depth", "1", repo_url, str(target_dir)], check=True, capture_output=True, text=True)
    return str(target_dir)
