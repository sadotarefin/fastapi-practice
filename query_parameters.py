from fastapi import FastAPI

app = FastAPI()

fake_items_db = [{
    "itema_name": "Foo"
},{
    "itema_name": "Bar"
},{
    "itema_name": "Baz"
}]

@app.get("/items/")
async def read_item(skip: int  = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

@app.get("/items/{item_id}")
async def read_item2(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short: 
        item.update(
            {
                "description": "this is an amazing item that has a long description"
            }
        )
    return item

@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, needy: str, q: str | None = None, short: bool = False
):
    item = {"item_id": item_id, "ownder_id": user_id, "needy": needy} #needy is required
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {
                "description": "This is an amazing item that has a long description"
            }
        )
    return item