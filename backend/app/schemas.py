from pydantic import BaseModel

class Item(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class Message(BaseModel):
    message: str