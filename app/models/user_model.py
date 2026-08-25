from sqlalchemy import Integer,Boolean,String
from sqlalchemy.orm import Mapped,mapped_column
from app.database import Base

class User(Base):
    __tablename__ = 'users'

    id : Mapped[int] = mapped_column(Integer,primary_key=True,index=True)
    email:Mapped[str]=mapped_column(String,unique=True,nullable=False,index=True)
    hashed_password:Mapped[str]=mapped_column(String,nullable=False)
    is_active:Mapped[str]=mapped_column(Boolean,default=True)