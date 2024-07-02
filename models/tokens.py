import datetime
import jwt
import sqlalchemy as sa
from sqlmodel import Field
from pydantic import BaseModel
from models.base import Base
from config import settings

class InvalidToken(Base, table=True):
    __tablename__ = 'invalid_tokens'

    token: str
    created_at: datetime.datetime = Field(sa_column=sa.Column(sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()))

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: str | None = None