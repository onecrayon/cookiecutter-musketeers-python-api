"""api.models

Data models using SQLAlchemy declarative_base.

This module needs to hoist all models to the root-level. For instance:

    from .user import User

This allows the Alembic migration logic to automatically detect all models
(when running Alembic migrations it uses `from api import models` to expose
all models to the generation logic).
"""
