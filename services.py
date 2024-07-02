from fastapi import HTTPException, status, Query, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, create_engine

# models
from models.users import User
from models.tokens import TokenData, is_token_blacklisted

# local settings
from config import settings

import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_user(username: str):
    engine = create_engine(settings.DATABASE_URL, echo=True)
    with Session(engine) as session:
        return session.query(User).filter(User.username == username).one()


async def get_current_user_token(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY,
                             algorithms=[settings.ALGORITHM])
        email: str = payload.get("email")

        if is_token_blacklisted(token):
            raise credentials_exception
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except jwt.ExpiredSignatureError:
        raise credentials_exception
    except jwt.DecodeError:
        raise credentials_exception
    user = session.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user
