PUZZLE_PAYLOAD_VALID = {
    "groups": [
        {"description": "Fruits", "words": ["banana", "apple", "orange", "grape"]},
        {"description": "Colors", "words": ["red", "blue", "green", "yellow"]},
        {"description": "Animals", "words": ["cat", "dog", "bird", "fish"]},
        {"description": "Planets", "words": ["mercury", "venus", "earth", "mars"]},
    ]
}

PUZZLE_PAYLOAD_INVALID = {
    "groups": [
        {"description": "Fruits", "words": ["banana", "apple", "orange", "grape"]},
        {"description": "Colors", "words": ["red", "blue", "green", "yellow"]},
        {"description": "Planets", "words": ["mercury", "venus", "earth", "mars"]},
    ]
}


def make_group(group_name: int, word_count: int) -> dict:
    return {
        "description": f"Group {group_name}",
        "words": [f"Word {group_name}/{word}" for word in range(word_count)],
    }


def make_puzzle(
    group_count: int,
    word_count: int,
    duplicate_words: bool = False,
    duplicate_description: bool = False,
) -> list[dict]:
    data = [make_group(group, word_count) for group in range(group_count)]
    if duplicate_description:
        data[0]["description"] = data[1]["description"]
    if duplicate_words:
        data[0]["words"][0] = data[1]["words"][1]
    return data
