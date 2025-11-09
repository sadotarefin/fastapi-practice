from datetime import datetime, time, timedelta
from typing import Annotated
from uuid import UUID
from pydantic import BaseModel

from fastapi import FastAPI, Body, Cookie, Header

app = FastAPI() 

class Cookies(BaseModel):
    model_config = {"extra":"forbid"}

    ads_id: str
    session_id: str
    fatebook_tracker: str | None = None
    googall_tracker: str | None = None

class CommonHeaders(BaseModel):
    host: str
    save_date: bool | None = None
    if_modified_since: str | None = None
    traceparent: str | None = None
    x_tag: list[str] = []
    accept: list[str] = []



@app.put("/items/{item_id}")
async def read_items(
    item_id: UUID, 
    start_datetime: Annotated[datetime, Body()],
    end_datetime: Annotated[datetime, Body()],
    process_after: Annotated[timedelta, Body()],
    repeat_at: Annotated[time | None, Body()] = None,
    #ads_id: Annotated[str | None,  Cookie()] = None,
    #user_agent: Annotated[str | None, Header()] = None,
    #x_token: Annotated[list[str] | None, Header()] = None,
    cookies: Annotated[Cookies, Cookie()] = None,
    headers: Annotated[CommonHeaders, Header()] = None
):
    start_process = start_datetime + process_after
    duration = end_datetime = start_process
    results ={
        "item_id": item_id,
        "start_datetime": start_process,
        "end_datetime": end_datetime,
        "repeat_at": repeat_at,
        "start_process": start_process,
        "duration": duration
    }
    #if ads_id:
      #  results.update({"ads_id": ads_id})
    #if user_agent:
      #  results.update({"User-Agent": user_agent})
    #if x_token:
      #  results.update({"X-Token": x_token})
    if cookies:
        results.update({"my-cookies": cookies})
    if headers:
        results.update({"headers": headers})
    return results