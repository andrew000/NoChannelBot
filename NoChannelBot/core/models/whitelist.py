from pydantic import BaseModel


class WhiteList(BaseModel):
    chat_id: int
    sender_chat_id: int
