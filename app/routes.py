from fastapi import APIRouter
from app.schemas import PuzzleCreate, PuzzleCreateResponse, PuzzleRead
from app.dependencies import SessionDependency
from uuid import UUID
from app.services import (
    create_puzzle_service,
    retrieve_puzzle_service,
)

router = APIRouter(prefix="/puzzles", tags=["puzzles"])


@router.post("/", status_code=201)
def create_puzzle(payload: PuzzleCreate, session: SessionDependency) -> PuzzleCreateResponse: # fmt: skip
    puzzle = create_puzzle_service(session, payload)
    return PuzzleCreateResponse(id=puzzle.id)


@router.get(path="/{puzzle_id}", response_model=PuzzleRead)
def retrieve_puzzle(puzzle_id: UUID, session: SessionDependency) -> PuzzleRead:
    return retrieve_puzzle_service(session, puzzle_id)
