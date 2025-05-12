from typing import Annotated
from fastapi import FastAPI, Path, Query, status, Body, HTTPException
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

# class Item(BaseModel):
#     description: str | None = None
#     text: str = "Simple text"

# class Message(BaseModel):
#     id: int
#     description: str = Field(..., description="The description of the message", max_length=300)
#     text: str = "Simple text"
#     created: datetime = Field(default_factory=datetime.now)
#     item: Item





class Message(BaseModel):
    id: int | None = None
    text: str
    
    model_config = {
        "json_schema_extra": {
            "examples":
                [
                    {
                        "text": "Simple message",
                    }
                ]
        }
    }


app = FastAPI()

messages_db = []


@app.get("/")
async def get_all_messages() -> dict:
    return {"Messages": messages_db}


@app.get("/message/{message_id}")
async def get_message(message_id: int) -> dict:
    try:
        return messages_db[message_id]
    except IndexError:
        raise HTTPException(status_code=404, detail="Mess Not Found")

@app.post("/message", status_code=status.HTTP_201_CREATED)
async def create_message(message: Message) -> str:
    if messages_db:
        message.id = max(messages_db, key=lambda m: m.id).id + 1
    else:
        message.id = 0
    messages_db.append(message)
    return "Mess created!"


@app.put("/message/{message_id}")
async def update_message(message_id: int, message: str = Body()) -> str:
    try:
        edit_message = messages_db[message_id]
        edit_message.text = message
        return "Message updated!"
    except IndexError:
        raise HTTPException(status_code=404, detail="Message not found")


@app.delete("/message/{message_id}")
async def delete_message(message_id: int) -> str:
    try:
        messages_db.pop(message_id)
        return f"Message ID={message_id} deleted!"
    except IndexError:
        raise HTTPException(status_code=404, detail="Message not found")


@app.delete("/")
async def kill_message_all() -> str:
    messages_db.clear()
    return "All messages deleted!"