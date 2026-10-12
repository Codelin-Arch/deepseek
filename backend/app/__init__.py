# DeepSeek-style Code Intelligence Stack

A hybrid code search stack using:
- FastAPI backend
- Qdrant for vector search
- Meilisearch for lexical search
- sentence-transformers fallback for embeddings
- GitHub repo indexing and optional Gitee mirror automation

## Stack

- Backend: FastAPI
- Embedding provider: OpenAI (preferred) or local sentence-transformers
- Vector DB: Qdrant
- Search: Meilisearch
- UI: Simple static front-end served by FastAPI
