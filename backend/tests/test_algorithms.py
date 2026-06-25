"""Pruebas unitarias de los algoritmos de búsqueda (lógica pura)."""

from __future__ import annotations

from app.domain.algorithms.bfs import BFSStrategy
from app.domain.algorithms.dfs import DFSStrategy
from app.domain.algorithms.astar import AStarStrategy
from app.domain.models.maze import Maze, Position


def _maze() -> Maze:
    return Maze(
        [
            [0, 0, 0, 1, 0],
            [1, 1, 0, 1, 0],
            [0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0],
        ]
    )


START = Position(0, 0)
GOAL = Position(4, 4)


def test_bfs_finds_path():
    result = BFSStrategy().search(_maze(), START, GOAL)
    assert result.found is True
    assert result.path[0] == START
    assert result.path[-1] == GOAL
    assert result.nodes_explored > 0


def test_bfs_returns_shortest_path():
    # En costo uniforme, BFS debe dar la ruta mínima (>= distancia Manhattan).
    result = BFSStrategy().search(_maze(), START, GOAL)
    assert result.path_length == 8


def test_dfs_finds_path():
    result = DFSStrategy().search(_maze(), START, GOAL)
    assert result.found is True
    assert result.path[0] == START
    assert result.path[-1] == GOAL


def test_astar_matches_bfs_length():
    # A* con heurística admisible debe igualar la longitud óptima de BFS.
    bfs = BFSStrategy().search(_maze(), START, GOAL)
    astar = AStarStrategy().search(_maze(), START, GOAL)
    assert astar.found is True
    assert astar.path_length == bfs.path_length


def test_path_is_contiguous():
    # Cada paso de la ruta debe ser adyacente al anterior.
    result = BFSStrategy().search(_maze(), START, GOAL)
    for a, b in zip(result.path, result.path[1:]):
        assert abs(a.row - b.row) + abs(a.col - b.col) == 1
