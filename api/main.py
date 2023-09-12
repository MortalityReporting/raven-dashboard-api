import json, typing
from typing import Annotated
from fastapi import Depends, FastAPI, File, UploadFile, Response, status, HTTPException, Form
from fastapi.security import HTTPBearer, OAuth2PasswordBearer
from pydantic_settings import BaseSettings
from starlette.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from api.utils.database import create_connection
from api.services.eventhandler import getEventData
from api.utils.token import VerifyToken, userHasScope
from api.utils.file_writer import writeFileToDisk
from sqlalchemy import text, select
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
import api.models.DocumentReference as DocRef
from api.services.fhirclient import FhirClient

class Settings(BaseSettings):
    app_name: str = "Raven Dashboard API"
    version: str = "0.2.0"

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
fhir_client = FhirClient()

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
async def getAdminPanel(response: JSONResponse, token: str= Depends(token_auth_scheme)):
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



@app.post("/document", response_class=PrettyJSONResponse)
async def postDocument(file: UploadFile, userId: Annotated[str, Form()], registrationId: Annotated[str, Form()]):
    try:
        file_name = writeFileToDisk(file)
        file_attachment: DocRef.Attachment = DocRef.Attachment(file_name)
        content: DocRef.Content = DocRef.Content(file_attachment)
        reference: DocRef.Reference = DocRef.Reference(f'Practitioner/{userId}')
        docref = DocRef.DocumentReference(reference, content)
        fhir_response = fhir_client.createResource("DocumentReference", docref.toJSON())
    except HTTPException as e:
        raise e
    else:
        return {
                "details": f'Successfully uploaded {file.filename}.',
                "resource": docref,
                "response": fhir_response
            }

@app.get("/document")
async def getDocument(file_name: str, response: JSONResponse, token: str= Depends(token_auth_scheme)):
    """A valid access token is required to access this route"""
    result = VerifyToken(token.credentials).verify()
    if result.get("status"):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return result
    
    scope_result = userHasScope("admin", result)
    if not scope_result:
        response.status_code = status.HTTP_403_FORBIDDEN
        return {
            "error": "Missing Permission",
            "message": "Missing proper scopes to access files, if this is a mistake please contact the Raven Administrators."
        }
    return FileResponse(f"users/{file_name}")