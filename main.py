from fastapi import FastAPI, Body, HTTPException, Depends
from schema.request import CreateTodoRequest
from schema.response import ToDoListSchema, ToDoSchema
from sqlalchemy.orm import Session
from typing import List

from database.connection import get_db
from database.repository import get_todos, get_todo_by_todo_id, create_todo, update_todo, delete_todo

from database.orm import ToDo

app = FastAPI()

@app.get("/")
def health_check_handler():
    return {"ping":"pong"}


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
def create_todo_handler(
        request: CreateTodoRequest,
        session: Session = Depends(get_db),
) -> ToDoSchema:
    todo = ToDo.create(request=request) # id None
    todo: ToDo = create_todo(session=session, todo=todo)    # id int
    return ToDoSchema.from_orm(todo)


# 할 일 수정
@app.patch("/todos/{todo_id}", status_code=200)
def update_todo_handler(
        todo_id: int,
        is_done: bool = Body(..., embed=True),
        session: Session = Depends(get_db),
):
    todo: ToDo | None = get_todo_by_todo_id(session=session, todo_id=todo_id)

    if todo:
        # update
        todo.done() if is_done else todo.undone()
        todo : ToDo = update_todo(session=session, todo=todo)
        return ToDoSchema.from_orm(todo)
    raise HTTPException(status_code=404, detail="ToDo Not Found")

# 할 일 삭제
@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo_handler(
        todo_id: int,
        session: Session = Depends(get_db),
):
    todo: ToDo | None = get_todo_by_todo_id(session=session, todo_id=todo_id)

    if not todo:
        raise HTTPException(status_code=404, detail="ToDo Not Found")

    delete_todo(session=session, todo_id=todo_id)
