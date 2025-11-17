from fastapi import BackgroundTasks, FastAPI, Depends
from typing import Annotated

app = FastAPI()


def write_notification(email: str, message: str = ""):
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)
    print("notificaiton sent")

def write_log(message: str):
    with open("qlog.txt", mode="a+") as qlog_file:
        content = f"Log for {message}"
        qlog_file.write(content)

def get_query(background_tasks: BackgroundTasks, q: str | None = None):
    if q:
        message = f"Found query: {q}: \n"
        background_tasks.add_task(write_log, message)
    return q

@app.post("/send-notification/{email}")
async def send_notification(email:str, background_task: BackgroundTasks, q: Annotated[str, Depends(get_query)]):
    background_task.add_task(write_notification, email, "hello world!")
    return {"message": "notification sent to background", "q": q}