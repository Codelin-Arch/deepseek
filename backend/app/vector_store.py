import json
import uuid
from typing import Any, Dict, List, Optional

from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import Distance, VectorParams

from app.config import QDRANT_COLLECTION, QDRANT_URL, LOCAL_EMBEDDING_MODEL, OPENAI_API_KEY, OPENAI_MODEL


class VectorStore:
    def __init__(self, collection_name: str = QDRANT_COLLECTION):
        self.client = QdrantClient(url=QDRANT_URL, timeout=30)
        self.collection_name = collection_name
        self._ensure_collection()

    def _ensure_collection(self):
        try:
            self.client.get_collection(self.collection_name)
        except Exception:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE),
            )

    def upsert_points(self, points: List[Dict[str, Any]]) -> None:
        payload = []
        for point in points:
            payload.append(
                models.PointStruct(
                    id=str(uuid.uuid4()),
                    vector=point["vector"],
                    payload=point["payload"],
                )
            )
        if payload:
            self.client.upsert(collection_name=self.collection_name, wait=True, points=payload)

    def search(self, vector: List[float], limit: int = 8, filter_payload: Optional[Dict[str, Any]] = None):
        search_filter = None
        if filter_payload:
            search_filter = models.Filter(**{"must": [models.FieldCondition(key=k, match=models.MatchValue(value=v)) for k, v in filter_payload.items()]})
        return self.client.search(
            collection_name=self.collection_name,
            query_vector=vector,
            query_filter=search_filter,
            limit=limit,
            with_payload=True,
        )

    def get_all(self, limit: int = 20):
        return self.client.scroll(collection_name=self.collection_name, limit=limit, with_payload=True)


vector_store = VectorStore()
