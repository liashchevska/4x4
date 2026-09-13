from app.models import Puzzle
from uuid import UUID, uuid4
from factories import PUZZLE_PAYLOAD_VALID, PUZZLE_PAYLOAD_INVALID


def test_create_puzzle_valid_data(client, session):
    response = client.post(url="/puzzles", json=PUZZLE_PAYLOAD_VALID)
    data = response.json()

    assert response.status_code == 201
    assert data.keys() == {"id"}

    puzzle = session.get(Puzzle, UUID(data["id"]))
    assert puzzle is not None


def test_create_puzzle_invalid_data(client):
    response = client.post(url="/puzzles", json=PUZZLE_PAYLOAD_INVALID)
    assert response.status_code == 422


def test_retrieve_puzzle_valid_id(client, puzzle):
    response = client.get(f"/puzzles/{puzzle.id}")
    data = response.json()

    assert response.status_code == 200
    assert "words" in data
    assert "groups" not in data


def test_retrieve_puzzle_invalid_id(client):
    non_existent_id = uuid4()
    response = client.get(f"/puzzles/{non_existent_id}")

    assert response.status_code == 404


def test_guess_correct_guess(client, puzzle):
    group = puzzle.groups[0]
    guess = {"words": group.word_ids}
    response = client.post(f"/puzzles/{puzzle.id}/guess", json=guess)

    assert response.status_code == 200

    actual = response.json()
    expected = {
        "group": {"title": group.title, "words": group.word_ids},
        "correct": True,
        "oneaway": False,
    }

    assert actual == expected


def test_guess_oneaway_guess(client, puzzle):
    group = puzzle.groups[0]
    guess = {"words": group.word_ids}
    guess["words"][0] = -1

    response = client.post(f"/puzzles/{puzzle.id}/guess", json=guess)

    assert response.status_code == 200

    actual = response.json()
    expected = {
        "group": None,
        "correct": False,
        "oneaway": True,
    }

    assert actual == expected


def test_guess_incorrect_guess(client, puzzle):
    guess = {"words": [-1] * 4}
    response = client.post(f"/puzzles/{puzzle.id}/guess", json=guess)

    assert response.status_code == 200

    actual = response.json()
    expected = {
        "group": None,
        "correct": False,
        "oneaway": False,
    }

    assert actual == expected
