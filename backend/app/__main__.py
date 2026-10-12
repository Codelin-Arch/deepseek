from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse

def create_app() -> FastAPI:
    app = FastAPI(title="DeepSeek-style code intelligence")
    return app
