from sqlmodel import Field
from datetime import datetime
from .base import Base


class Url(Base, table=True):
    __tablename__ = "urls"

    long_url: str
    short_url: str
    title: str
    user_id: int | None = Field(default=None, foreign_key="users.id")
    creation_date: datetime = Field(default_factory=datetime.utcnow)
