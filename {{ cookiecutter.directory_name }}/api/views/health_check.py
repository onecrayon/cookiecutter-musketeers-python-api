{% if cookiecutter.framework == "FastAPI" -%}
from enum import Enum
import logging

from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel
from sqlalchemy.sql.expression import literal_column

from api import get_session


logger = logging.getLogger(__name__)

router = APIRouter()


class HealthCheckStatusResponses(str, Enum):
    """Output strings for status responses"""

    okay = "okay"
    error = "error"


class HealthCheckServicesOut(BaseModel):
    """Nested services status tracking"""

    database: HealthCheckStatusResponses = HealthCheckStatusResponses.okay

    def __iter__(self):
        """Allow iterating over the various services for easy checking for failures"""
        return iter((self.database,))


class HealthCheckOut(BaseModel):
    """Information about API system status"""

    status: HealthCheckStatusResponses = HealthCheckStatusResponses.okay
    services: HealthCheckServicesOut = HealthCheckServicesOut()

    @property
    def has_errors(self):
        if any(x == HealthCheckStatusResponses.error for x in self.services):
            self.status = HealthCheckStatusResponses.error
            return True
        return False


# Construct example error output for OpenAPI spec
_error_out_example = HealthCheckOut()
_error_out_example.services.database = HealthCheckStatusResponses.error
_error_out_example = _error_out_example.has_errors and _error_out_example.dict()


@router.get(
    "/health-check",
    tags=["server"],
    response_model=HealthCheckOut,
    responses={
        status.HTTP_503_SERVICE_UNAVAILABLE: {
            "description": "One or more services are down",
            "content": {"application/json": {"example": _error_out_example}},
        }
    },
)
def health_check(response: Response, session: db.Session = Depends(get_session)):
    """Reports on service and overall API status. Please do not hit this endpoint repeatedly;
    it is mainly intended for diagnosing problems internally."""
    # Default okay response
    output = HealthCheckOut()

    # Check for PostgreSQL database health
    try:
        meaning_of_life_the_universe_and_everything = session.query(
            literal_column("42")
        ).scalar()
        assert meaning_of_life_the_universe_and_everything == 42
    except:
        output.services.database = HealthCheckStatusResponses.error
        logger.error("Postgres health-check FAILED", exc_info=True)

    if output.has_errors:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    return output

{% elif cookiecutter.framework == "Falcon 3 (WSGI)" -%}
import logging

import falcon
from sqlalchemy.sql.expression import literal_column


logger = logging.getLogger(__name__)


class HealthCheck:
    """Check internal systems for faults"""
    def on_get(self, req: falcon.Request, resp: falcon.Response):
        # Default okay response
        resp.media = {
            'status': 'okay',
            'services': {
                'database': 'okay',
            }
        }
        # Verify that the database is up and running
        try:
            meaning_of_life_the_universe_and_everything = req.context.session.query(
                literal_column("42")
            ).scalar()
            assert meaning_of_life_the_universe_and_everything == 42
        except:
            logger.error("Postgres health-check FAILED", exc_info=True)
            resp.status = falcon.HTTP_SERVICE_UNAVAILABLE
            resp.media['status'] = 'error'
            resp.media['services']['database'] = 'error'

{% else -%}
import logging

import falcon
from sqlalchemy import select
from sqlalchemy.sql.expression import literal_column


logger = logging.getLogger(__name__)

class HealthCheck:
    """Check internal systems for faults"""
    async def on_get(self, req: falcon.Request, resp: falcon.Response):
        # Default okay response
        resp.media = {
            'status': 'okay',
            'services': {
                'database': 'okay',
            }
        }
        # Verify that the database is up and running
        try:
            meaning_of_life_the_universe_and_everything = await req.context.session.execute(
                select(literal_column("42"))
            ).scalar()
            assert meaning_of_life_the_universe_and_everything == 42
        except:
            logger.error("Postgres health-check FAILED", exc_info=True)
            resp.status = falcon.HTTP_SERVICE_UNAVAILABLE
            resp.media['status'] = 'error'
            resp.media['services']['database'] = 'error'

{% endif %}
