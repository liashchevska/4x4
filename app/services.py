from sqlalchemy.orm import Session
from app.models import Puzzle
from app.schemas import PuzzleCreate


def create_puzzle_service(session: Session, payload: PuzzleCreate) -> Puzzle:
    puzzle = Puzzle.create(session, data=payload)
    session.commit()
    session.refresh(puzzle)
    return puzzle
