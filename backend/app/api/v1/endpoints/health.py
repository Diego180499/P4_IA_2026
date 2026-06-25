"""Endpoint de salud del servicio."""

from __future__ import annotations

from fastapi import APIRouter

from app.core.config import settings

router = APIRouter(tags=["health"])


@router.get("/health", summary="Verifica que el servicio está activo")
def health() -> dict[str, str]:
    return {"status": "ok", "service": settings.PROJECT_NAME, "version": settings.VERSION}
