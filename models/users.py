from sqlmodel import Field
from .base import Base

class User(Base, table=True):
    __tablename__ = "users"

    username: str = Field(sa_column_kwargs={"unique": True})