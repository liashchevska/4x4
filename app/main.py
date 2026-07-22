from typing import Annotated
from fastapi import Depends, FastAPI
from .database import Session, get_session

SessionDep = Annotated[Session, Depends(get_session)]


app = FastAPI()


@app.get("/")
async def root():
    return "Nothing here yet!"
