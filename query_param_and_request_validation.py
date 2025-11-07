from typing import Annotated

from fastapi import FastAPI, Query
from pydantic import AfterValidator
import random

app = FastAPI()

data = {
    "isbn-121": "Hello world",
    "imdb-121": "hello world movie"
}

def check_valid_id(id: str):
    #print("hel")
    if not id.startswith(("isbn-", "imdb-")):
        raise ValueError("Invalid ID format, it must start with 'isbn-' or 'imdb-'")
    return id


@app.get("/items/")
async def read_items(
    q: Annotated[
                 str|None,
                 #str | None, 
                 #Query(min_length = 5, max_length=50, pattern="^fixedquery$")] = None
                 #Query(min_length = 5, max_length=50 )] = "fixedquery"
                 Query(min_length = 3)]
                 ):
    result = {
        "items":[
            {
                "item_id": "Foo"
            },
            {
                "item_id": "Bar"
            }
        ]
    }
    if q:
        result.update({"q": q})
    return result

@app.get("/items/{item_id}")
async def read_items(item_id : int = 0,
                     id: Annotated[str | None, AfterValidator(check_valid_id)] = None,
                     q : Annotated[
                         list[str] | None, Query(title="Query String", min_length=2, alias="my-q")
                     ] = None,
                     qq : Annotated[str | None, Query(title="Hidden Query", include_in_schema=False)] = None):
    query_items = {"q": q, "id": id}
    if qq:
        query_items.update({"qq":qq})
    if id:
        query_items.update({"id": id, "name": data.get(id)})
    else:
        #print(data.items())
        id, item = random.choice(list(data.items()))
        query_items.update({"id": id, "name": item})
    return query_items


