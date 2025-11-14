from typing import Annotated
from fastapi import FastAPI, Depends, Cookie

app = FastAPI()

fake_item_db = [
    {"item_name": "foo"}, {"item_name": "bar"}, {"item_name": "baz"}
]

class CommonQueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit

async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return { "q": q, "skip": skip, "limit": limit }

CommonDep = Annotated[dict, Depends(common_parameters)]

def query_extractor(q: str | None = None):
    return q

def query_or_cookie_extractor(q: Annotated[str, Depends(query_extractor)],
                              last_query: Annotated[str | None, Cookie()] = None):
    if not q:
        last_query
    return q


@app.get("/items/")
async def read_items(common: Annotated[CommonQueryParams, Depends()], query_or_default: Annotated[str, Depends(query_or_cookie_extractor)]):
    response = {}
    if common.q:
        response.update({"common_q": common.q})
    items = fake_item_db[common.skip : common.skip + common.limit]
    response.update({"items": items})
    response.update({"q_or_cookie": query_or_default})
    return response

@app.get("/users/")
async def read_users(common: CommonDep):
    return common