from fastapi import FastAPI, Form
from typing import Annotated
from pydantic import BaseModel

app = FastAPI()

class LoginFormData(BaseModel):
    username: str
    password: str
    model_config = {"extra": "forbid"}


@app.post("/login/", response_model=LoginFormData, response_model_exclude={"password"})
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    return {"username": username, "password": password}

@app.post("/login2/", response_model=LoginFormData, response_model_exclude={"password"})
async def login(data: Annotated[LoginFormData, Form()]):
    return data

