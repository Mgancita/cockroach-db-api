"""Build and serve the api."""

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from v1.routers import health, student

os.environ["TZ"] = "UTC"
title_detail = os.getenv("PROJECT_ID", "Local")
version = os.getenv("SHORT_SHA", "local")

api = FastAPI(title=f"Cockroach DB API: {title_detail}", version=version)

# CORS
api.add_middleware(
    CORSMiddleware,
    allow_methods=["*"],
    allow_origins=["*"]
)

# /
api.include_router(health.router)

# /v1
api_v1_prefix = "/v1"
api.include_router(student.router, prefix=api_v1_prefix)
