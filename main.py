import uvicorn
from fastapi import FastAPI, HTTPException, status, Depends, Query
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from datetime import timedelta
from db import get_session

from models.urls import Url
from models.users import User
from models.tokens import Token, TokenData, create_access_token
from config import settings
from services import get_current_user_token, get_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
import jwt

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

@app.get("/")
def root():
    return {"message": "Root Route"}


@app.get('/urls', status_code=200)
async def get_links(session: Session = Depends(get_session)):
    statement = select(Url)
    results = session.exec(statement).all()
    return results

@app.post('/urls/add', status_code=200)
async def add_link(url_data: Url, session: Session = Depends(get_session)):
    new_link = Url(**url_data.model_dump())
    session.add(new_link)
    session.commit()
    session.refresh(new_link)
    return {"Url added:": new_link.title}

@app.post('/users/add')
async def add_user(user_data: User, session: Session = Depends(get_session)):
    new_user = User(**user_data.model_dump())
    new_user.hashed_password = User.hash_password(new_user.hashed_password);
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return { "User added:", new_user.username }


@app.post('/login', status_code=200)
async def login(user_data: User):
    # try:
    user: User = get_user(username=user_data.username)
    print(f"USER IS?? {user}")
    # except:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Invalid user credentials"
    #     )

    is_validated: bool = user.validate_password(user_data.hashed_password)

    if not is_validated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user credentials"
        )

    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"username": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=8000, reload=True)