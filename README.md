# DeepSeek-style Code Intelligence Stack

A production-minded repository for indexing and searching public/private GitHub codebases with vector search + lexical search, a FastAPI service, and a simple browser UI.

## Highlights

- Hybrid retrieval: Qdrant (vector) + Meilisearch (keyword)
- OpenAI embedding support with local fallback
- One-click GitHub repo indexing
- Gitee sync workflow for faster domestic access
- Browser-based query UI

## Quick start

1. Copy `.env.example` to `.env` and fill values.
2. Start the stack:
   ```bash
   docker compose up --build
   ```
3. Open the app at http://localhost:8000/
4. Submit a repo URL or local folder path to index and search.

## Environment variables

See `.env.example`.

## Index a repo

You can either:

- Use the browser UI, or
- Call the API directly:

```bash
curl -X POST http://localhost:8000/api/index/repo \
  -H 'Content-Type: application/json' \
  -d '{"repo_url": "https://github.com/tiangolo/fastapi"}'
```

Search:

```bash
curl -X POST http://localhost:8000/api/search \
  -H 'Content-Type: application/json' \
  -d '{"query": "how does dependency injection work in FastAPI"}'
```

## Local development

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Architecture

- Backend: FastAPI + Python
- Vector store: Qdrant
- Full-text index: Meilisearch
- Storage: local /data/repos
- Embeddings: OpenAI text-embedding-3-small or local sentence-transformers

## Gitee sync

A GitHub Actions workflow is included to mirror the repository to Gitee.
Set the following secrets in GitHub:

- `GITEE_SSH_KEY`
- `GITEE_HOST`

Optional:

- `OPENAI_API_KEY`

## Notes

- For private repos, use a PAT or SSH auth and avoid sharing secrets in public spaces.
- Keep GitHub repo mirrors within compliance and licensing constraints.
