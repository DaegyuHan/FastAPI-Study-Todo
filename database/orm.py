from importlib.resources import contents

from schema.request import CreateTodoRequest
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class ToDo(Base):
    __tablename__ = "todo"

    id = Column(Integer, primary_key=True, index=True)
    contents = Column(String(256), nullable=False)
    is_done = Column(Boolean, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"))

    def __repr__(self):
        return f"ToDo(id={self.id}, contents={self.contents}, is_done={self.is_done})"

    @classmethod
    def create(cls, request: CreateTodoRequest) -> "ToDo":
        return cls(
            contents = request.contents,
            is_done = request.is_done,
        )

    def done(self) -> "ToDo":
        self.is_done = True
        return self

    def undone(self) -> "ToDo":
        self.is_done = False
        return self


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(256), nullable=False)
    password = Column(String(256), nullable=False)
    email = Column(String(256), nullable=True)
    todos = relationship("ToDo", lazy="joined")

    @classmethod
    def create(cls, username: str, hashed_password: str) -> "User":
        return cls(
            username=username,
            password=hashed_password,
        )

    def update_email(self, email: str):
        self.email = email
        return self