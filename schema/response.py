from pydantic import BaseModel
from typing import List

class ToDoSchema(BaseModel):
    id: int
    contents: str
    is_done: bool

    class Config:
        from_attributes = True

class ToDoListSchema(BaseModel):
    todos: List[ToDoSchema]


class UserSchema(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True