from sqlalchemy.orm import Session, selectinload
from app.models import Puzzle, Group
from app.schemas import PuzzleIn
from uuid import UUID
from sqlalchemy import select
from app.exceptions import PuzzleDoesNotExist

def create_puzzle_service(session: Session, payload: PuzzleIn) -> Puzzle:
    puzzle = Puzzle.create(session, group_list=payload.model_dump()["groups"])
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
