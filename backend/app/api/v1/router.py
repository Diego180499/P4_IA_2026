"""Agrupa todos los routers de la versión 1 de la API."""

from __future__ import annotations

from fastapi import APIRouter

from app.api.v1.endpoints import health, mazes, search

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(mazes.router)
api_router.include_router(search.router)
