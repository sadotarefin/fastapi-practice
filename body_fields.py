#use after validator somewherre for practice
from typing import Annotated

from fastapi import Body, FastAPI
from pydantic import BaseModel, Field, HttpUrl

app = FastAPI()

class Image(BaseModel):
    url: HttpUrl
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
    thumbs: list[Image] | None = None

class Offer(BaseModel):
    name: str
    description: str | None = None
    price: float
    items: list[Item]

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
    results = {"item_id": item_id, "item": item}
    return results

@app.post("/offers/")
async def create_offer(offer: Offer):
    return offer

@app.post("/images/multiple/")
async def create_multiple_images(images: list[Image]):
    return images

@app.post("/index-weights/")
async def create_index_weights(weights: dict[int, float]):
    return weights