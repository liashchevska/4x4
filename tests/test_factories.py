from factories import make_group, make_puzzle

def test_make_group():
    group = make_group(1, 4)
    assert group == {
        "description": "Group 1",
        "words": ["Word 1/0", "Word 1/1", "Word 1/2", "Word 1/3"],
    }


def test_make_puzzle():
    puzzle = make_puzzle(2, 2)
    data = [
        {
            "description": "Group 0",
            "words": ["Word 0/0", "Word 0/1"],
        },
        {
            "description": "Group 1",
            "words": ["Word 1/0", "Word 1/1"],
        },
    ]
    assert puzzle == data


def test_make_puzzle_with_duplicate_descriptions():
    puzzle = make_puzzle(2, 2, duplicate_description=True)
    assert puzzle[0]["description"] == puzzle[1]["description"]


def test_make_puzzle_with_duplicate_words():
    puzzle = make_puzzle(2, 2, duplicate_words=True)
    words = [word for group in puzzle for word in group["words"]]
    assert len(set(words)) != len(words)
