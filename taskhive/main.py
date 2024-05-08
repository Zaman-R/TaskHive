from typing import Annotated

from fastapi import FastAPI, Depends, Path, HTTPException

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

