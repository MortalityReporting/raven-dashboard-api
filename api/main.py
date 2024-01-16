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
import os
from api.services.miniohandler import MinioClient
from api.constants import ERRORS

class Settings(BaseSettings):
    app_name: str = "Raven Dashboard API"
    version: str = "0.3.0"

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
minio_client = MinioClient()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

"""
Provides basic information about the application.
"""
@app.get("/info", response_class=PrettyJSONResponse)
async def info():
    return {"Application": settings.app_name, "Version": settings.version}

"""
This endpoint provides the configuration for the Raven Dashboard and does not contain sensitive information.
"""
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

"""
Provides access to the Admin Panel for verified users.
"""
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
            "code": response.status_code,
            "error": ERRORS['SECURITY_ERRORS']['MISSING_PERMISSIONS']['NAME'],
            "message": ERRORS['SECURITY_ERRORS']['MISSING_PERMISSIONS']['DESC'],
        }

    req = getEventData()
    return req


"""
Allows users to upload a file from a test to Minio.
"""
@app.post("/document", response_class=PrettyJSONResponse)
async def postFile(file: UploadFile, event: Annotated[str, Form()], response: JSONResponse, token: str = Depends(token_auth_scheme)):
    """A valid access token is required to access this route"""
    result = VerifyToken(token.credentials).verify()
    if result.get("status"):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return result
    
    scope_result = userHasScope("admin", result)
    if not scope_result:
        response.status_code = status.HTTP_403_FORBIDDEN
        return {
            "code": response.status_code,
            "error": ERRORS['SECURITY_ERRORS']['MISSING_PERMISSIONS']['NAME'],
            "message": ERRORS['SECURITY_ERRORS']['MISSING_PERMISSIONS']['DESC'],
        }
    try: 
        result = minio_client.uploadToMinio(file=file, bucket_name=event)
    except HTTPException as e:
        raise e
    else:
        return {
            "bucket": result.bucket_name,
            "filename": result.object_name
        }

@app.get("/document")
async def getFile(file_name: str, event: str, response: JSONResponse, token: str= Depends(token_auth_scheme)):
    """A valid access token is required to access this route"""
    result = VerifyToken(token.credentials).verify()
    if result.get("status"):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return result
    
    scope_result = userHasScope("admin", result)
    if not scope_result:
        response.status_code = status.HTTP_403_FORBIDDEN
        print(ERRORS)
        return {
            "code": response.status_code,
        }
    return FileResponse(f"users/{file_name}")

@app.get("/document/all")
async def getAllDocuments(response: JSONResponse, token: str= Depends(token_auth_scheme)):
    result = VerifyToken(token.credentials).verify()
    if result.get("status"):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return result
    
    scope_result = userHasScope("admin", result)
    if not scope_result:
        response.status_code = status.HTTP_403_FORBIDDEN
        return {
            "code": response.status_code,
            "error": ERRORS['SECURITY_ERRORS']['MISSING_PERMISSIONS']['NAME'],
            "message": ERRORS['SECURITY_ERRORS']['MISSING_PERMISSIONS']['DESC'],
        }
    file_list = os.listdir("users")
    return (file_list)
