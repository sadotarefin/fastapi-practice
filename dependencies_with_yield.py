from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException, status

app = FastAPI()

class InternalError(Exception):
    pass

@app.exception_handler

def get_username():
    try:
        yield "Rick" #simulate getting current username
    except InternalError:
        print("We do not shallow the interal exception here, we raise them")
        raise
    finally:
        print("cleaning up")

@app.get("/items/{item_id}")
async def read_item(item_id: str, username: Annotated[str, Depends(get_username)]):
    if item_id == 'portal-gun':
        raise InternalError(f"Portal gun cannot be owned by {username}")
    if item_id != 'foo':
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "item not found"
        )
    print("Sending response back")
    return item_id

