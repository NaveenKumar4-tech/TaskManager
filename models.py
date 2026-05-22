from sqlalchemy import Column,Integer,String,Boolean,ForeignKey
from database import Base
from sqlalchemy.orm import relationship

class User(Base):

    __tablename__="users"

    id=Column(Integer,primary_key=True,index=True)

    username=Column(String)
    email=Column(String)
    password=Column(String)


class Task(Base):

    __tablename__="tasks"

    id=Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,ForeignKey("users.id"))
    title=Column(String,nullable=False)
    note=Column(String,nullable=True)
    status = Column(Boolean,default=False)
    user = relationship("User")