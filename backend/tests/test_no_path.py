"""Prueba del caso en que no existe ruta válida (manejo de errores)."""

from __future__ import annotations

from app.domain.algorithms.bfs import BFSStrategy
from app.domain.algorithms.dfs import DFSStrategy
from app.domain.models.maze import Maze, Position


def _enclosed_maze() -> Maze:
    # La meta (2,2) está rodeada por muros.
    return Maze(
        [
            [0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0],
            [0, 1, 0, 1, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0],
        ]
    )


def test_bfs_no_path():
    result = BFSStrategy().search(_enclosed_maze(), Position(0, 0), Position(2, 2))
    assert result.found is False
    assert result.path == []


def test_dfs_no_path():
    result = DFSStrategy().search(_enclosed_maze(), Position(0, 0), Position(2, 2))
    assert result.found is False
    assert result.path == []
