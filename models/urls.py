from sqlmodel import Field
import datetime
from .base import Base

class Urls(Base, table=True):
    __tablename__ = "urls"

    long_url: str
    short_url: str
    title: str
    user_id: int | None = Field(default=None, foreign_key="users.id")
    creation_date: datetime.datetime