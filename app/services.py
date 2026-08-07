from sqlalchemy.orm import Session, selectinload
from app.models import Puzzle, Group
from app.schemas import PuzzleCreate
from uuid import UUID
from sqlalchemy import select


class PuzzleDoesNotExist(Exception):
    pass


def create_puzzle_service(session: Session, payload: PuzzleCreate) -> Puzzle:
    puzzle = Puzzle.create(session, data=payload)
    session.commit()
    session.refresh(puzzle)
    return puzzle


def retrieve_puzzle_service(session: Session, puzzle_id: UUID) -> Puzzle:
    stmt = (
        select(Puzzle)
        .options(selectinload(Puzzle.groups).selectinload(Group.words))
        .where(Puzzle.id == puzzle_id)
    )
    puzzle = session.scalar(stmt)

    if puzzle is None:
        raise PuzzleDoesNotExist()
    return puzzle
