from fastapi import FastAPI, HTTPException, status, Request
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHttpException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from fastapi.exception_handlers import (
    http_exception_handler as heh
)

app = FastAPI()

class Item(BaseModel):
    name: str
    code: int = Field(..., ge=1, le=100)

class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name

@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exec: UnicornException):
    return JSONResponse(
        status_code=status.HTTP_417_EXPECTATION_FAILED,
        content={
            "message": f"Oops! {exec.name} has done something bad!!!"
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exec: RequestValidationError):
    #return PlainTextResponse(str(exec), status_code=status.HTTP_418_IM_A_TEAPOT)
    print("Catched...")
    return JSONResponse(
        status_code=status.HTTP_418_IM_A_TEAPOT,
        content=jsonable_encoder({
            "detail": exec.errors,
            "body": exec.body
        })
         )

@app.exception_handler(StarletteHttpException)
async def http_exception_handler(request: Request, exce: StarletteHttpException):
    #return PlainTextResponse(str(exce), status_code=exce.status_code)
    print("this is called")
    return await heh(request, exce)

items= {
    'foo': {'name': "product 1", "code": 1}
}

@app.get("/items/{item_id}")
async def read_items(item_id: str, name: int | None = None):
    if item_id not in items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": "item not found"}, headers={"asdf":"asdf"})
    if name:
        raise UnicornException(name = name)
    return {"item_id": item_id, "item": Item(**items[item_id])}

@app.post("/items/")
async def create_item(item: Item):
    return item