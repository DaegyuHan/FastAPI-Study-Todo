from fastapi import FastAPI, Body, HTTPException
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def health_check_handler():
    return {"ping":"pong"}

todo_data = {
    1: {
        "id": 1,
        "contents": "한대규의 오늘 할 일1",
        "is_done": True
    },
    2: {
        "id": 2,
        "contents": "한대규의 오늘 할 일2",
        "is_done": False
    },
    3: {
    "id": 3,
        "contents": "한대규의 오늘 할 일3",
        "is_done": False
    }
}

# 할 일 전체 조회
@app.get("/todos", status_code=200)
def get_todos_handler(order: str | None = None):
    ret = list(todo_data.values())
    if order == "DESC":
        return ret[::-1]
    return ret

# 할 일 단일 조회
@app.get("/todos/{todo_id}", status_code=200)
def get_todo_handler(todo_id: int):
    todo = todo_data.get(todo_id)
    if todo:
        return todo
    raise HTTPException(status_code=404, detail="ToDo Not Found")

class CreateTodoRequest(BaseModel):
    id: int
    content: str
    is_done: bool

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
