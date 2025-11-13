from fastapi import FastAPI, Response
from pydantic import BaseModel, EmailStr
from fastapi.responses import RedirectResponse, JSONResponse
from typing import Any

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float = 10.5
    tax: float | None = None
    tags: list[str] = []

class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None

items = {
    "foo": { "name": "Foo", "price": 100},
    "bar": { "name": "Bar", "price": 200, "description": "Bar Projedt", "price": 63, "tax": 120},
    "buz": { "name": "Baz", "price": 100, "description": None,  "price": 63, "tax": 12, "tags": ['t1']}
}

@app.post("/items/")
async def create_item(item: Item) -> Item: 
    return item

@app.get("/items/{item_id}", response_model=Item, response_model_exclude={"tags"}) #this exclude works
async def read_item(item_id: str):
    return items[item_id]

@app.get("/items/", response_model=list[Item], 
         response_model_exclude_unset=True,
         response_model_exclude={"tax"}) #response_mode_exclude does not work for list items
async def read_items() -> Any:
    return [
        { "name": "Foo", "price": 100},
        { "name": "Bar", "description": "Bar Projedt", "tax": 120}
    ]

@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: Item):
    return {
        "item_id": item_id,
        "name": item.name,
        "price": 120.00
    }

@app.post("/user/")
async def create_user(user: UserIn):
    return user

@app.get("/portal", response_model=None)
async def get_port(teleport: bool = False, json: bool = False) -> Response | dict:
    if teleport:
        return RedirectResponse(url="https://www.youtube.com")
    if json:
        return JSONResponse(content={"msg": "helloworl"})
    return {"asdfadsf": "dafasdf"}


