from pydantic import BaseModel


class CreateTodoRequest(BaseModel):
    contents: str
    is_done: bool

class SignUpRequest(BaseModel):
    username: str
    password: str

class SignInRequest(BaseModel):
    username: str
    password: str

class CreateOTPRequest(BaseModel):
    email: str