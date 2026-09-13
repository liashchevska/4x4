from app.utils import is_unique


def test_is_unique():
    assert is_unique(["apple", "banana", "cherry"])
    assert not is_unique(["apple", "banana", "BANANA"])
