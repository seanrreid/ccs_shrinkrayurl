from fastapi import Query, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session

# models
from models.users import User
from models.tokens import TokenData, is_token_blacklisted

# local settings
from db import get_session
from config import settings

import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_user(username: str, session: Session = Depends(get_session)):
    return session.query(User).filter(User.username == username).one()


async def get_current_user_token(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):

    try:
        payload = jwt.decode(token, settings.SECRET_KEY,
                             algorithms=[settings.ALGORITHM])
        email: str = payload.get("email")

        if is_token_blacklisted(token):
            raise settings.CREDENTIALS_EXCEPTION
        if email is None:
            raise settings.CREDENTIALS_EXCEPTION
        token_data = TokenData(email=email)
    except jwt.ExpiredSignatureError:
        raise settings.CREDENTIALS_EXCEPTION
    except jwt.DecodeError:
        raise settings.CREDENTIALS_EXCEPTION
    user = session.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user
