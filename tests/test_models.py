import pytest
from sqlalchemy import select, func
from app.models import Group, Puzzle, Word
from app.schemas import PuzzleCreate
from tests.factories import make_puzzle


@pytest.fixture
def puzzle(session):
    puzzle = Puzzle()
    session.add(puzzle)
    session.flush()
    return puzzle


@pytest.fixture
def group(session, puzzle):
    group = Group(description="Mammals", puzzle=puzzle)
    session.add(group)
    session.flush()
    return group


def test_add_group_to_puzzle(session, puzzle, group):
    """Ensure a group added to a puzzle is persisted correctly."""
    puzzle.groups.append(group)
    session.commit()

    retrieved_group = session.get(Group, group.id)
    assert retrieved_group is not None
    assert retrieved_group.puzzle_id == puzzle.id


def test_add_word_to_group(session, group):
    """Ensure a word added to a group is persisted correctly."""

    word = Word(text="Cat")
    group.words.append(word)
    session.commit()

    retrieved_word = session.get(Word, word.id)
    assert retrieved_word is not None
    assert retrieved_word.group_id == group.id


def test_groups_and_words_deleted_along_with_puzzle(session, puzzle, group):
    """Ensure deleting a puzzle removes its groups and words."""

    word = Word(text="Cat")
    group.words.append(word)
    session.commit()

    session.delete(puzzle)
    session.commit()

    assert session.get(Group, group.id) is None
    assert session.get(Word, word.id) is None


def test_create_puzzle_creates_groups_and_words(session):
    """Test that Puzzle.create method creates Words, Groups along with Puzzle."""
    group_count, word_count = 4, 4
    data = make_puzzle(group_count, word_count)

    puzzle = Puzzle.create(session, data=PuzzleCreate(groups=data))

    stmt = select(func.count(Group.id)).where(Group.puzzle_id == puzzle.id)
    assert session.scalar(stmt) == group_count

    stmt = select(func.count(Word.id)).join(Group).where(Group.puzzle_id == puzzle.id)
    assert session.scalar(stmt) == group_count * word_count
