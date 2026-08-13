import pytest
from sqlalchemy import select, func
from app.models import Group, Puzzle, Word, GuessResult
from app.schemas import PuzzleCreate
from tests.factories import make_puzzle


@pytest.fixture
def empty_puzzle(session):
    puzzle = Puzzle()
    session.add(puzzle)
    session.flush()
    return puzzle


@pytest.fixture
def empty_group(session, empty_puzzle):
    group = Group(title="Mammals", puzzle=empty_puzzle)
    session.add(group)
    session.flush()
    return group


def test_add_group_to_puzzle(session, empty_puzzle, empty_group):
    """Ensure a group added to a puzzle is persisted correctly."""
    empty_puzzle.groups.append(empty_group)
    session.commit()

    retrieved_group = session.get(Group, empty_group.id)
    assert retrieved_group is not None
    assert retrieved_group.puzzle_id == empty_puzzle.id


def test_add_word_to_group(session, empty_group):
    """Ensure a word added to a group is persisted correctly."""

    word = Word(text="Cat")
    empty_group.words.append(word)
    session.commit()

    retrieved_word = session.get(Word, word.id)
    assert retrieved_word is not None
    assert retrieved_word.group_id == empty_group.id


def test_groups_and_words_deleted_along_with_puzzle(session, empty_puzzle, empty_group):
    """Ensure deleting a puzzle removes its groups and words."""

    word = Word(text="Cat")
    empty_group.words.append(word)
    session.commit()

    session.delete(empty_puzzle)
    session.commit()

    assert session.get(Group, empty_group.id) is None
    assert session.get(Word, word.id) is None


def test_create_puzzle_creates_groups_and_words(session):
    """Test that Puzzle.create method creates Words, Groups along with Puzzle."""
    group_count, word_count = 4, 4
    data = make_puzzle(group_count, word_count)

    puzzle = Puzzle.create(session, group_list=data)

    stmt = select(func.count(Group.id)).where(Group.puzzle_id == puzzle.id)
    assert session.scalar(stmt) == group_count

    stmt = select(func.count(Word.id)).join(Group).where(Group.puzzle_id == puzzle.id)
    assert session.scalar(stmt) == group_count * word_count


def test_words_property(session):
    group_count, word_count = 4, 4
    data = make_puzzle(group_count, word_count)

    puzzle = Puzzle.create(session, group_list=data)
    assert len(puzzle.words) == group_count * word_count


def test_group_guess_correct(puzzle):
    group = puzzle.groups[0]
    guess = [word.id for word in group.words]

    assert group.guess(guess) == GuessResult.CORRECT


def test_group_guess_oneaway(puzzle):
    group = puzzle.groups[0]
    guess = [word.id for word in group.words]
    guess[0] = puzzle.groups[1].words[0].id

    assert group.guess(guess) == GuessResult.ONEAWAY


def test_group_guess_incorrect(puzzle):
    group = puzzle.groups[0]
    guess = [puzzle.groups[i].words[i].id for i in range(4)]

    assert group.guess(guess) == GuessResult.INCORRECT


def test_puzzle_guess_correct(puzzle):
    group = puzzle.groups[0]
    guess = [word.id for word in group.words]

    assert puzzle.guess(guess) == (GuessResult.CORRECT, group)


def test_puzzle_guess_oneaway(puzzle):
    group = puzzle.groups[0]
    guess = [word.id for word in group.words]
    guess[0] = puzzle.groups[1].words[0].id

    assert puzzle.guess(guess) == (GuessResult.ONEAWAY, None)


def test_puzzle_guess_incorrect(puzzle):
    guess = [puzzle.groups[i].words[i].id for i in range(4)]

    assert puzzle.guess(guess) == (GuessResult.INCORRECT, None)
