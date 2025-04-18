from pydantic import BaseModel, PositiveInt

class Item(BaseModel):
    item_id: PositiveInt
    cups: PositiveInt

class User(BaseModel):
    username: str
    password: str