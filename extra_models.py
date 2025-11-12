from fastapi import FastAPI, status
from pydantic import BaseModel, EmailStr, Field
from typing import Annotated, Union, Literal

app = FastAPI()

class UserBase(BaseModel):
    username: str 
    email: EmailStr
    full_name: str | None = None

class UserIn(UserBase):
    password: str 

class UserOut(UserBase):
    pass

class UserInDb(UserBase): 
    hashed_password: str 

class BaseItem(BaseModel):
    description: str
    kind: str

class CarItem(BaseItem):
    kind: Literal["car"]

class PlaneItem(BaseItem):
    kind: Literal["plane"]
    #size: int

ItemUnion = Annotated[Union[CarItem, PlaneItem], Field(discriminator="kind")]

items = {
    "item1": {
        "description": "All my friends drive a low rider", "kind": "car"
    },
    "item2": {
        "description": "Music is my aeroplane, it' my asdfadf",
        "kind": "plane",
        "size": 5
    }
}

def fake_password_hasher(raw_password: str):
    return 'sadfadf' + raw_password

def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDb(**user_in.model_dump(), hashed_password=hashed_password)
    print("User saved! .. not really")
    return user_in_db

@app.post("/user/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved

@app.get("/item/{item_id}", response_model= ItemUnion)
async def read_item(item_id: str):
    item = items[item_id] 
    return item