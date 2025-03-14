from pydantic import BaseModel
from typing import List

class ToDoSchema(BaseModel):
    id: int
    contents: str
    is_done: bool

    class Config:
        from_attributes = True

class ListToDoResponse(BaseModel):
    todos: List[ToDoSchema]