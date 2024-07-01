import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from db import get_session

from models.urls import Url
from models.users import User

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
    new_link = Url(**url_data.dict())
    session.add(new_link)
    session.commit()
    session.refresh(new_link)
    return {"Url added:": new_link.title}


if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=8000, reload=True)