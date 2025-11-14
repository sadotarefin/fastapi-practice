from fastapi import FastAPI, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    tax: float = 10.5
    tags: list[str] = []

items = {
    "foo": {"name": "Foo", "description": "Foo is a good name"},
    "bar": {"name": "Bar", "description": "Description of bar", "price": 20.3, "tax": ".5"},
    "baz": {"name": "Baz", "description": "Baz is another good foo", "price": "12", "tax": .12, "tags": ["adfafd"]}
}

@app.get("/items/{item_id}", response_model=Item)
async def read_items(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return items[item_id]

@app.put("/items/{item_id}", response_model=Item)
async def update_items(item_id: str, item: Item):
    if item_id not in items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    items[item_id] = jsonable_encoder(item)
    return items[item_id]

@app.patch("/items/{item_id}", response_model=Item)
async def update_items(item_id: str, item: Item):
    if item_id not in items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    stored_item_data = items[item_id]
    stored_item_model = Item(**stored_item_data)
    updated_data = item.model_dump(exclude_unset=True)
    updated_model = stored_item_model.model_copy(update=updated_data)
    items[item_id] = jsonable_encoder(updated_model)
    return updated_model