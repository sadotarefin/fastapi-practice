from typing import Annotated, Literal
from fastapi import FastAPI, Query
from pydantic import BaseModel, Field
from enum import Enum

app = FastAPI()

class MyOrder(str, Enum):
    CREATED_AT = 'created_at'
    UPDATED_AT = 'updated_at'
    

class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal[MyOrder.CREATED_AT, MyOrder.UPDATED_AT] = MyOrder.CREATED_AT
    tags: list[str] = []

class Item(BaseModel):
    name: str
    description: str | None = Field(default=None, examples=["A very good example"]) #this will work in case no model_config
    price: float
    tax: float | None = None

    model_config = {
        "json_schema_extra": {
            "examples":[{
                "name": "Foo",
                "description": "A very nice Item",
                "price": 35.4,
                "tax": 2.3
            }
            ]
        }
    }

@app.get("/items/")
async def read_items(filter_query: Annotated[FilterParams, Query()]):
    return filter_query

@app.post("/items/")
async def create_items(item: Item):
    return item