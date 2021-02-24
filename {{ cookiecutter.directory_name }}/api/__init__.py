"""api

The root application module.

`api.environment` includes environment variables via Pydantic settings:

    from api.environment import settings
"""
# Hoist the app for easier access
from .main import app
