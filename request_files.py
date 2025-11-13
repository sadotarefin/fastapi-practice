from fastapi import FastAPI, File, UploadFile, Form
from typing import Annotated

app = FastAPI()

@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"filesize": len(file)}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filesize": file.size, "filename": file.filename}

@app.post("/files2/")
async def file_with_form(
    file: Annotated[bytes, File()],
    fileb: UploadFile,
    token: Annotated[str, Form()]
):
    return {
        "file": len(file),
        "fileb": fileb.content_type,
        "token": token
    }