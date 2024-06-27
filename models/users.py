from .base import Base

class User(Base, table=True):
    __tablename__ = "users"