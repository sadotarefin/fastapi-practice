from typing import Annotated
from fastapi import FastAPI, HTTPException, Depends, Header, status

async def verify_token(x_token: Annotated[str, Header()]):
    if x_token != "fake_super_secret_token":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="X-Token header invalid")

async def verify_key(x_key: Annotated[str, Header()]):
    if x_key != "fake_super_secret_key":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="X-Key header invalid")
    return x_key

app = FastAPI(dependencies=[Depends(verify_key), Depends(verify_key)])


#@app.get("/items/" ''', dependencies=[Depends(verify_token), Depends(verify_key)]''')
@app.get("/items/")
async def read_items():
    return [
        {"name": "item 1"},
        {"name": "item 2"}
    ]