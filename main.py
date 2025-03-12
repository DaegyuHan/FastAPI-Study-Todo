from fastapi import FastAPI

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

@app.get("/todos")
def get_todos_handler():
    return list(todo_data.values())