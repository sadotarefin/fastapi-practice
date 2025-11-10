from typing import Any
from fastapi import FastAPI, Response
from pydantic import BaseModel, EmailStr
from fastapi.responses import JSONResponse, RedirectResponse

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []

class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None

class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None

@app.post("/items/")
async def create_item(item: Item) -> Item:
    return item

@app.get("/items/", response_model=list[Item], response_model_exclude_unset=True, response_model_exclude={"tax"})
#async def read_items() -> list[Item]:
async def read_items() -> Any:
    return [
        Item(name="Product 1", price=43.10),
        Item(name="Product x", price="2405", tags=["good", "better"], tax=12.4)
    ]

@app.post("/user/", response_model=UserOut)
async def create_user(user: UserIn) -> Any:
    return user


@app.get("/portal/")
async def get_portal(teleport: bool = False) -> Response:
    if teleport:
        return RedirectResponse(url="www.youtube.com")
    return JSONResponse(content={"message": "dasfasdf"})