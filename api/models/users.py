from sqlmodel import Field
from pydantic import EmailStr

import bcrypt

from .base import Base

class User(Base, table=True):
    __tablename__ = "users"

    username: EmailStr = Field(nullable=False, sa_column_kwargs={"unique": True})
    hashed_password: str = Field(nullable=False)

    @staticmethod
    def hash_password(password) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def validate_password(self, password) -> bool:
        return bcrypt.checkpw(password=password.encode(), hashed_password=self.hashed_password.encode())