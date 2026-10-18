from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.exceptions import PuzzleDoesNotExist, puzzle_does_not_exist_exception_handler
from app.routes import router

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
)

app.add_exception_handler(PuzzleDoesNotExist, puzzle_does_not_exist_exception_handler)
app.include_router(router)
