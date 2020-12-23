"""Configures the main API app and routes"""
import logging

{% if cookiecutter.framework == "FastAPI" -%}
from fastapi import FastAPI
{%- else -%}
import falcon
{%- endif %}
{% if cookiecutter.framework == "Falcon 3 (ASGI)" -%}
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
{% else -%}
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
{% endif -%}

from .environment import settings

__version__ = "{{ cookiecutter.version }}"

# Configure our logging level
logging.basicConfig(level=logging.WARNING if not settings.debug else logging.DEBUG)

{% if cookiecutter.framework == "Falcon 3 (ASGI)" -%}
engine = create_async_engine(settings.postgres_url, echo=settings.debug)
{% else -%}
# Setup base SQLAlchemy engine and session class
engine = create_engine(settings.postgres_url, echo=settings.debug)
SessionLocal = sessionmaker(bind=engine)
{% endif -%}

# Setup our declarative base; this keeps migration-generated indexes consistently named
meta = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)
AlchemyBase = declarative_base(metadata=meta)

{% if cookiecutter.framework == "FastAPI" -%}
# Setup our database dependency
def get_session():
    """Primary database dependency"""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

# Create our main application
app = FastAPI(
    title="{{ cookiecutter.project_name }}",
    description=(
        "{{ cookiecutter.project_description }}"
    ),
    version=__version__,
    docs_url="/",
    redoc_url="/redoc",
)
{% elif cookiecutter.framework == "Falcon 3 (WSGI)" -%}
# Setup session middleware to configure the database connection
class SQLAlchemySessionManager:
    """Falcon middleware to create an SQLAlchemy session for every request, and close it when the request ends.

    Access to session is available through `req.context.session`.

    Automatically closes the session when the request is complete (but doesn't roll anything back, currently).

    Inspired by <https://eshlox.net/2019/05/28/integrate-sqlalchemy-with-falcon-framework-second-version>"""
    def process_resource(self, req: falcon.Request, resp, resource, params):
        if req.method == 'OPTIONS':
            return

        req.context.session = SessionLocal()

    def process_response(self, req: falcon.Request, resp, resource, req_succeeded: bool):
        if req.method == 'OPTIONS':
            return

        if 'session' in req.context:
            req.context.session.close()

# Create our main application
app = falcon.App(middleware=[
    SQLAlchemySessionManager(),
])
{% elif cookiecutter.framework == "Falcon 3 (ASGI)" -%}
class SQLAlchemySessionManager:
    """Falcon middleware to create an SQLAlchemy session for every request, and close it when the request ends.

    Access to session is available through `req.context.session`.

    Automatically closes the session when the request is complete (but doesn't roll anything back, currently).

    Inspired by <https://eshlox.net/2019/05/28/integrate-sqlalchemy-with-falcon-framework-second-version>"""
    async def process_resource(self, req: falcon.Request, resp, resource, params):
        if req.method == 'OPTIONS':
            return

        req.context.session = AsyncSession(engine)

    async def process_response(self, req: falcon.Request, resp, resource, req_succeeded: bool):
        if req.method == 'OPTIONS':
            return

        if 'session' in req.context:
            req.context.session.close()

# Create our main application
app = falcon.asgi.App(middleware=[
    SQLAlchemySessionManager(),
])
{%- endif %}

# A health-check route is required to deploy on Render.com
from api.views import health_check  # noqa
{% if cookicutter.framework == "FastAPI" -%}
app.include_router(health_check.router)
{% else -% }
app.add_route('/health-check', health_check.HealthCheck())
{%- endif %}

# TODO: define other API routes, include routers, etc. here
