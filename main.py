from fastapi import FastAPI, Body, HTTPException, Depends
from schema.request import CreateTodoRequest
from schema.response import ToDoListSchema, ToDoSchema
from sqlalchemy.orm import Session
from typing import List

from database.connection import get_db
from database.repository import get_todos, get_todo_by_todo_id

from database.orm import ToDo

app = FastAPI()

@app.get("/")
def health_check_handler():
    return {"ping":"pong"}

# todo_data = {
#     1: {
#         "id": 1,
#         "contents": "한대규의 오늘 할 일1",
#         "is_done": True
#     },
#     2: {
#         "id": 2,
#         "contents": "한대규의 오늘 할 일2",
#         "is_done": False
#     },
#     3: {
#     "id": 3,
#         "contents": "한대규의 오늘 할 일3",
#         "is_done": False
#     }
# }

# 할 일 전체 조회
@app.get("/todos", status_code=200)
def get_todos_handler(
        order: str | None = None,
        session: Session = Depends(get_db),
):
    todos: List[ToDo] = get_todos(session=session)

    if order == "DESC":
        return ToDoListSchema(
        todos=[ToDoSchema.from_orm(todo) for todo in todos[::-1]]
    )
    return ToDoListSchema(
        todos=[ToDoSchema.from_orm(todo) for todo in todos]
    )

# 할 일 단일 조회
@app.get("/todos/{todo_id}", status_code=200)
def get_todo_handler(
        todo_id: int,
        session: Session = Depends(get_db),
) -> ToDoSchema:

    todo: ToDo | None = get_todo_by_todo_id(session=session, todo_id=todo_id)

    if todo:
        return ToDoSchema.from_orm(todo)
    raise HTTPException(status_code=404, detail="ToDo Not Found")


# 할 일 생성
@app.post("/todos", status_code=201)
def create_todo_handler(request: CreateTodoRequest):
    todo_data[request.id] = request.dict()
    return

# 할 일 수정
@app.patch("/todos/{todo_id}", status_code=200)
def update_todo_handler(
        todo_id: int,
        is_done: bool = Body(..., embed=True),
):
    todo = todo_data.get(todo_id)
    if todo:
        todo["is_done"] = is_done
        return todo
    raise HTTPException(status_code=404, detail="ToDo Not Found")

# 할 일 삭제
@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo_handler(todo_id: int):
    todo = todo_data.pop(todo_id, None)
    if todo:
        return
    raise HTTPException(status_code=404, detail="ToDo Not Found")
