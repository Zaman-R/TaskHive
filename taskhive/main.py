from typing import Annotated

from fastapi import FastAPI, Depends, Path, HTTPException
from pydantic import BaseModel, Field

from sqlalchemy.orm import Session
from starlette import status

from models import Todo
from database import engine, SessionLocal
import models

app = FastAPI()

models.Base.metadata.create_all(bind=engine)  # create everything


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

class TodoRequest(BaseModel):
    tittle: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(ge=0, le=10)
    complete: bool


@app.get("/")
async def read_all(db: db_dependency):  # dependency injection , this fuctions relys on get_db()
    return db.query(Todo).all()


@app.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todo).filter(Todo.id == todo_id).first()
    print(todo_model)

    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not found")


@app.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, todo: TodoRequest):
    todo_model = Todo(**todo.dict())
    db.add(todo_model)
    db.commit()