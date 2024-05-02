from database import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey

class Todo(Base):
    __tablename__ = 'todos'


    id = Column(Integer, primary_key=True, index=True)
    tittle = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
