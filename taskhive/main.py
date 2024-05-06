from typing import Annotated

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import models
from database import engine, SessionLocal

app = FastAPI()

models.Base.metadata.create_all(bind=engine)  # create everything


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def read_all(db: Annotated[Session, Depends(get_db)]):  # dependency injection , this fuctions relys on get_db()
    return db.query(models.Todo).all()
