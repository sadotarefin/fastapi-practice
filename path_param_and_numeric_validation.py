from typing import Annotated
from fastapi import FastAPI, Path, Query

app = FastAPI()


@app.get("/items/{item_id}")
async def read_items(
    item_id: Annotated[int , Path(
        ge=1,
        title="The ID of the item to get", 
        description="formal description")],
    q: Annotated[str | None, Query(alias="item-query")] = None,
    size: Annotated[float | None, Query(gt=0, lt=10.5)] = None
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if size:
        results.update({"size": size})
    return results