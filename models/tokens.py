import jwt
import sqlalchemy as sa
from datetime import datetime, timedelta, timezone
from sqlmodel import Field, Session
from pydantic import BaseModel
from fastapi import Depends

from models.base import Base

from db import get_session
from config import settings

class InvalidToken(Base, table=True):
    __tablename__ = 'invalid_tokens'

    token: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: str | None = None

# Details in the docs here:
# https://fastapi.tiangolo.com/tutorial/secur≠ity/oauth2-jwt/#update-the-token-path-operation

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    # Make a copy so we don't mutate the original data
    to_encode = data.copy()

    if expires_delta:
        # If an expires_delta is provided, the expiration time (expire) is set to the current UTC time plus the  delta.
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # If expires_delta is not provided, the default expiration time is set to 15 minutes from the current UTC time.
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    # Add the expiration to the JWT
    to_encode.update({"exp": expire})
    # Actually encode our JWT with the data/time settings
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return encoded_jwt


def is_token_blacklisted(token, session: Session = Depends(get_session)):
    # Check if the token is blacklisted in the database
    return session.query(BlacklistedToken).filter_by(token=token).first() is not None
