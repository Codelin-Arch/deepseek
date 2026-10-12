import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[2] / ".env")

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
REPOS_DIR = DATA_DIR / "repos"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "text-embedding-3-small")
LOCAL_EMBEDDING_MODEL = os.getenv("LOCAL_EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
APP_PORT = int(os.getenv("APP_PORT", "8000"))

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "deepseek_code")

MEILI_URL = os.getenv("MEILI_URL", "http://localhost:7700")
MEILI_MASTER_KEY = os.getenv("MEILI_MASTER_KEY", "")
MEILI_INDEX = os.getenv("MEILI_INDEX", "code_chunks")

GITHUB_DEFAULT_REPO = os.getenv("GITHUB_DEFAULT_REPO", "tiangolo/fastapi")

REPOS_DIR.mkdir(parents=True, exist_ok=True)


def get_openai_enabled() -> bool:
    return bool(OPENAI_API_KEY)
