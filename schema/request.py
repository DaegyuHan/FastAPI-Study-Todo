from pydantic import BaseModel


class CreateTodoRequest(BaseModel):
    id: int
    content: str
    is_done: bool
