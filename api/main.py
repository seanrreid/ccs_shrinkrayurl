import uvicorn
import jwt
from typing import Annotated
from datetime import timedelta
from fastapi import FastAPI, Depends, status, HTTPException, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from sqlmodel import Session, select
from nanoid import generate
from db import get_session
from config import settings

from models.urls import Url
from models.users import User
from models.tokens import Token, TokenData, InvalidToken, create_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Setup our origins...
# ...for now it's just our local environments
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173",
]

app = FastAPI()

# Add the CORS middleware...
# ...this will pass the proper CORS headers
# https://fastapi.tiangolo.com/tutorial/middleware/
# https://fastapi.tiangolo.com/tutorial/cors/
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def lookup_user(username: str, session: Session = Depends(get_session)):
    statement = select(User).where(User.username == username)
    return session.exec(statement).first()


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY,
                             algorithms=[settings.ALGORITHM])
        username: str = payload.get("username")

        if username is None:
            raise settings.CREDENTIALS_EXCEPTION

        token_data = TokenData(username=username)
    except:
        raise settings.CREDENTIALS_EXCEPTION
    return token_data


@app.get("/")
def root():
    return {"message": "Root Route"}


@app.get('/urls', status_code=200)
async def get_links(session: Session = Depends(get_session)):
    statement = select(Url)
    results = session.exec(statement).all()
    return results


@app.get("/sendit")
async def redirect_to_external_url(url: str = Query(...), session: Session = Depends(get_session)):
    # The ellipsis (...) is a special value in FastAPI that
    # indicates the parameter is required.
    # It means that the "url" parameter must be present
    # in the request, and its value must not be None.

    # Find the long url via the short
    statement = select(Url).where(Url.short_url == url)
    link = session.exec(statement).first()

    # Add the https protocol
    long_url = f"https://{link.long_url}"

    # redirect
    return RedirectResponse(long_url)


@app.post('/urls/add', status_code=200)
async def add_link(url_data: Url, user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    if user is not None:
        new_link = Url(**url_data.model_dump())
        new_link.short_url = generate(size=8)
        session.add(new_link)
        session.commit()
        session.refresh(new_link)
        return {"Url added:": new_link.title}
    else:
        raise settings.CREDENTIALS_EXCEPTION


@app.get('/users/current', status_code=200)
async def get_user_id(current_user: str = Depends(get_current_user), session: Session = Depends(get_session)):
    user_info = lookup_user(current_user.username, session)
    return {"username": user_info.username, "id": user_info.id}


@app.post('/users/add')
async def add_user(user_data: User, session: Session = Depends(get_session)):
    new_user = User(**user_data.model_dump())
    new_user.hashed_password = User.hash_password(new_user.hashed_password)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return {"User added:", new_user.username}


@app.post("/login", status_code=200)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: Session = Depends(get_session)):
    try:
        user = lookup_user(form_data.username, session)
    except:
        raise settings.CREDENTIALS_EXCEPTION

    is_validated: bool = user.validate_password(form_data.password)

    if not is_validated:
        raise settings.CREDENTIALS_EXCEPTION

    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"username": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@app.get('/logout', status_code=200)
def logout(token: Token = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    try:
        invalid_token = InvalidToken(token=token)
        session.add(invalid_token)
        session.commit()
    except:
        raise settings.CREDENTIALS_EXCEPTION
    return {"details:": "Logged out"}


if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=8000, reload=True)
