"""API router for health servies."""

from datetime import datetime
import os
from typing import Any, Dict

from fastapi import APIRouter

router = APIRouter()


@router.get("/healthcheck", tags=["public"])
def healthcheck() -> Dict[str, Any]:
    """Check if the API is awake."""
    message = "alive and kicking"
    version = os.getenv("SHORT_SHA", "local")
    response = {"message": message, "version": version, "time": datetime.utcnow()}
    return response
