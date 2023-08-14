import json, typing
from fastapi import Depends, FastAPI, Response, status
from fastapi.security import HTTPBearer, OAuth2PasswordBearer
from pydantic_settings import BaseSettings
from starlette.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from api.services.database import create_connection
from api.services.fhir import getEventData
from api.utils.token import VerifyToken, userHasScope
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

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={"admin": "Able to access admin panel."},
)

token_auth_scheme = HTTPBearer()
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
    
@app.get("/admin-panel", response_class=PrettyJSONResponse)
def private(response: JSONResponse, token: str= Depends(token_auth_scheme)):
    """A valid access token is required to access this route"""
    result = VerifyToken(token.credentials).verify()
    scope_result = userHasScope("admin", result)

    if result.get("status"):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return result
    
    if not scope_result:
        response.status_code = status.HTTP_403_FORBIDDEN
        return {
            "error": "Missing Permission",
            "message": "Missing proper scopes to access administrative view, if this is a mistake please contact the Raven Administrators."
        }

    req = getEventData()
    return req