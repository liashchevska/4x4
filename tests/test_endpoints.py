from app.models import Puzzle
from uuid import UUID
from factories import PUZZLE_PAYLOAD_VALID, PUZZLE_PAYLOAD_INVALID

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
