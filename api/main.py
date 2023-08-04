import json, typing
from fastapi import FastAPI, Request
from pydantic_settings import BaseSettings
from starlette.responses import Response
import requests
import os
from fastapi.staticfiles import StaticFiles
from urllib.parse import urljoin
from fastapi.middleware.cors import CORSMiddleware
from api.services.database import create_connection
from sqlalchemy import text, select
from sqlalchemy.orm import Session

class Settings(BaseSettings):
    app_name: str = "Raven Dashboard API"
    version: str = "0.1.0"

class PrettyJSONResponse(Response):
    media_type = "application/json"
    def render(self, content: typing.Any) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=4,
            separators=(", ", ": "),
        ).encode("utf-8")

settings = Settings()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/info", response_class=PrettyJSONResponse)
async def info():
    return {"Application": settings.app_name, "Version": settings.version}

@app.get("/config", response_class=PrettyJSONResponse)
async def getConfig(env: str = "dev"):
    engine = create_connection(True)
    statement = f'SELECT json FROM dashboard.configuration WHERE env_id = \'{env}\' limit 1;'
    with Session(engine) as session:
        result = session.execute(text(statement)).first()
    if result is None:
        return { 'error': f'No configuration for "{env}" found.'}
    else:
        return result[0]