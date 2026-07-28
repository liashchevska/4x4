import pytest
from app.models import Group, Puzzle, Word


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
