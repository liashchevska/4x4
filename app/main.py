from fastapi import FastAPI

from app.exceptions import PuzzleDoesNotExist, puzzle_does_not_exist_exception_handler
from app.routes import router

app = FastAPI()

app.add_exception_handler(PuzzleDoesNotExist, puzzle_does_not_exist_exception_handler)
app.include_router(router)
