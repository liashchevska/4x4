from pydantic import ValidationError
import pytest

from app.schemas import PuzzleCreate
from factories import make_puzzle


def test_puzzle_rejects_invalid_group_count():
    """Puzzle should contain 4 groups of words"""
    with pytest.raises(ValidationError):
        PuzzleCreate(groups=make_puzzle(3, 4))

    with pytest.raises(ValidationError):
        PuzzleCreate(groups=make_puzzle(5, 4))


def test_puzzle_accepts_four_groups():
    """A valid puzzle contains exactly four groups."""
    puzzle = PuzzleCreate(groups=make_puzzle(4, 4))
    assert len(puzzle.groups) == 4


def test_puzzle_rejects_non_unique_words():
    """Words must be unique across the puzzle."""
    with pytest.raises(ValidationError, match="Words must be unique"):
        PuzzleCreate(groups=make_puzzle(4, 4, duplicate_words=True))


def test_puzzle_rejects_non_unique_group_titles():
    """Titles must be unique across the puzzle."""
    with pytest.raises(ValidationError, match="Group titles must be unique"):
        PuzzleCreate(groups=make_puzzle(4, 4, duplicate_title=True))
