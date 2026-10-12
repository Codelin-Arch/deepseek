import os
import hashlib
from pathlib import Path
from typing import Iterable, List, Dict, Any

from sentence_transformers import SentenceTransformer
from openai import OpenAI

from app.config import OPENAI_API_KEY, OPENAI_MODEL, LOCAL_EMBEDDING_MODEL


class Embedder:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None
        self.model = SentenceTransformer(LOCAL_EMBEDDING_MODEL) if not self.client else None

    def embed(self, text: str) -> List[float]:
        if self.client:
            response = self.client.embeddings.create(model=OPENAI_MODEL, input=text)
            return response.data[0].embedding
        if self.model is None:
            raise RuntimeError("No embedding backend configured.")
        return self.model.encode(text).tolist()


embedder = Embedder()


def chunk_text(text: str, size: int = 600, overlap: int = 100) -> List[str]:
    lines = text.splitlines()
    windows: List[str] = []
    chunks: List[str] = []
    count = 0
    for line in lines:
        windows.append(line)
        count += 1
        if count >= size:
            chunks.append("\n".join(windows))
            windows = windows[-overlap:] if overlap > 0 else []
            count = len(windows)
    if windows:
        chunks.append("\n".join(windows))
    return chunks or [text]


def file_hash(path: str) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest() if Path(path).exists() else ""
