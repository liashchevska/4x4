from fastapi import APIRouter
from app.models import Puzzle
from app.schemas import PuzzleCreate, PuzzleCreateResponse, PuzzleRetrieve
from app.dependencies import SessionDependency
from app.services import create_puzzle_service

router = APIRouter(prefix="/puzzles", tags=["puzzles"])


@router.post("/", status_code=201)
def create_puzzle(payload: PuzzleCreate, session: SessionDependency) -> PuzzleCreateResponse: # fmt: skip
    puzzle = create_puzzle_service(session, payload)
    return PuzzleCreateResponse(id=puzzle.id)
