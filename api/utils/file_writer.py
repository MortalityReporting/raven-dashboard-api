from pathlib import Path
import shutil
from fastapi import UploadFile, HTTPException
from uuid import uuid4
import mimetypes


def writeFileToDisk(file: UploadFile):
    destination = Path("users")
    try:
        file_name = generateFileName(file)
    except HTTPException as e:
        raise e
    file_path = destination / file_name
    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    finally:
        file.file.close()
    return file_name


def generateFileName(file: UploadFile):
    # TODO: Add error handling if type returns None
    mime_type = mimetypes.guess_type(file.filename)[0]
    if mime_type is None:
        raise HTTPException(status_code=400, detail= "File type (mimetype) could not be detected. Please include a valid file type extension.")
    ext = mimetypes.guess_extension(mime_type)
    file_name = str(uuid4()) + ext
    return file_name