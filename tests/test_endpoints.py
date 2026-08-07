from app.models import Puzzle
from uuid import UUID

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


def test_create_puzzle_valid_data(client, session):
    response = client.post(url="/puzzles/", json=PUZZLE_PAYLOAD_VALID)
    data = response.json()

    assert response.status_code == 201
    assert data.keys() == {"id"}

    puzzle = session.get(Puzzle, UUID(data["id"]))
    assert puzzle is not None


def test_create_puzzle_invalid_data(client):
    response = client.post(url="/puzzles/", json=PUZZLE_PAYLOAD_INVALID)
    assert response.status_code == 422
