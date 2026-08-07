PUZZLE_PAYLOAD_VALID = {
    "groups": [
        {"title": "Fruits", "words": ["banana", "apple", "orange", "grape"]},
        {"title": "Colors", "words": ["red", "blue", "green", "yellow"]},
        {"title": "Animals", "words": ["cat", "dog", "bird", "fish"]},
        {"title": "Planets", "words": ["mercury", "venus", "earth", "mars"]},
    ]
}

PUZZLE_PAYLOAD_INVALID = {
    "groups": [
        {"title": "Fruits", "words": ["banana", "apple", "orange", "grape"]},
        {"title": "Colors", "words": ["red", "blue", "green", "yellow"]},
        {"title": "Planets", "words": ["mercury", "venus", "earth", "mars"]},
    ]
}


def make_group(group_name: int, word_count: int) -> dict:
    return {
        "title": f"Group {group_name}",
        "words": [f"Word {group_name}/{word}" for word in range(word_count)],
    }


def make_puzzle(
    group_count: int,
    word_count: int,
    duplicate_words: bool = False,
    duplicate_title: bool = False,
) -> list[dict]:
    data = [make_group(group, word_count) for group in range(group_count)]
    if duplicate_title:
        data[0]["title"] = data[1]["title"]
    if duplicate_words:
        data[0]["words"][0] = data[1]["words"][1]
    return data
