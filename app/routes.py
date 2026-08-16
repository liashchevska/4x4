from fastapi import APIRouter
from app.schemas import (
    PuzzleIn,
    PuzzleOut,
    PuzzleRead,
    GuessIn,
    GuessOut,
    GroupBase
)
from app.dependencies import SessionDependency
from uuid import UUID
from app.services import create_puzzle_service, retrieve_puzzle_service

router = APIRouter(prefix="/puzzles", tags=["puzzles"])


@router.post("/", status_code=201)
def create_puzzle(payload: PuzzleIn, session: SessionDependency) -> PuzzleOut: # fmt: skip
    puzzle = create_puzzle_service(session, payload)
    return PuzzleOut(id=puzzle.id)


@router.get(path="/{puzzle_id}", response_model=PuzzleRead)
def retrieve_puzzle(puzzle_id: UUID, session: SessionDependency):
    return retrieve_puzzle_service(session, puzzle_id)
