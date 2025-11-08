#use after validator somewherre for practice
from typing import Annotated

from fastapi import Body, FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class Image(BaseModel):
    url: str
    name: str

class Item(BaseModel):
    name: str
    description: str | None = Field(
        default=None, title = "The description of the item", max_length=100
    )
    price: float = Field(gt=0, description="The price must be greater than zero") 
    tax: float | None = None
    #tags: list[str] = []
    tags: set[str] = set() #as set
    image: Image | None = None

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
    results = {"item_id": item_id, "item": item}
    return results