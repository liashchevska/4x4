from fastapi.responses import JSONResponse
from fastapi import status, Request


class PuzzleDoesNotExist(Exception):
    pass


def puzzle_does_not_exist_exception_handler(request: Request, exc: PuzzleDoesNotExist):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND, content={"deatail": "Puzzle not found"}
    )
