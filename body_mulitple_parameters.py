from typing import Annotated

from fastapi import FastAPI, Path, Body
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

class User(BaseModel):
    username: str
    full_name: str | None = None


@app.put("/items/{item_id}")
async def update_item(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
    user: User | None = None,
    q: str | None = None,
    item: Item | None = None,
    importance: Annotated[int | None, Body()] = None
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    if user:
        results.update({"user": user})
    if importance:
        results.update({"importance": importance})
    return results

@app.post("/items")
async def create_item(item: Annotated[Item, Body(embed=True)]):
    results = {"item_id": 1, "item": item}
    return results
