from fastapi import APIRouter, HTTPException, status
from app.models import Puzzle
from app.schemas import PuzzleCreate, PuzzleCreateResponse, PuzzleRetrieve
from app.dependencies import SessionDependency
from uuid import UUID
from app.services import (
    create_puzzle_service,
    retrieve_puzzle_service,
    PuzzleDoesNotExist,
)

router = APIRouter(prefix="/puzzles", tags=["puzzles"])


@router.post("/", status_code=201)
def create_puzzle(payload: PuzzleCreate, session: SessionDependency) -> PuzzleCreateResponse: # fmt: skip
    puzzle = create_puzzle_service(session, payload)
    return PuzzleCreateResponse(id=puzzle.id)


@router.get(path="/{puzzle_id}", response_model=PuzzleRetrieve)
def retrieve_puzzle(puzzle_id: UUID, session: SessionDependency) -> PuzzleRetrieve:
    try:
        puzzle = retrieve_puzzle_service(session, puzzle_id)
    except PuzzleDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Puzzle not found"
        )
    return puzzle
