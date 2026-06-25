"""Pruebas de integración de los endpoints de la API."""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

_MAZE = {
    "grid": [
        [0, 0, 0, 1, 0],
        [1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0],
    ]
}
_START = {"row": 0, "col": 0}
_GOAL = {"row": 4, "col": 4}


def test_health():
    r = client.get("/api/v1/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_list_predefined_mazes():
    r = client.get("/api/v1/mazes")
    assert r.status_code == 200
    assert len(r.json()) >= 5  # mínimo 5 laberintos predefinidos


def test_get_maze_not_found():
    r = client.get("/api/v1/mazes/no-existe")
    assert r.status_code == 404


def test_search_bfs():
    r = client.post(
        "/api/v1/search",
        json={"maze": _MAZE, "start": _START, "goal": _GOAL, "algorithm": "bfs"},
    )
    assert r.status_code == 200
    body = r.json()
    assert body["found"] is True
    assert body["nodes_explored"] > 0
    assert body["path"][0] == _START
    assert body["path"][-1] == _GOAL


def test_search_invalid_algorithm():
    r = client.post(
        "/api/v1/search",
        json={"maze": _MAZE, "start": _START, "goal": _GOAL, "algorithm": "xyz"},
    )
    assert r.status_code == 400


def test_search_start_on_wall():
    r = client.post(
        "/api/v1/search",
        json={"maze": _MAZE, "start": {"row": 1, "col": 0}, "goal": _GOAL, "algorithm": "bfs"},
    )
    assert r.status_code == 422


def test_compare():
    r = client.post(
        "/api/v1/search/compare",
        json={"maze": _MAZE, "start": _START, "goal": _GOAL, "algorithms": ["bfs", "dfs"]},
    )
    assert r.status_code == 200
    body = r.json()
    assert "bfs" in body["results"]
    assert "dfs" in body["results"]
    assert body["comparison"]["shorter_path"] == "bfs"
