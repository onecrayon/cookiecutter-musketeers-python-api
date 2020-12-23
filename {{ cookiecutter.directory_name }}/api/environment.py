"""Configuration settings, loaded from environment variables

Typical usage:

    from api.environment import settings

## Adding new environment variables

You must define your new environment variable in 2-3 places:

1. Your environment:
    * LOCAL: `.env` to set the actual value
    * PRODUCTION: actual environment variables (`.env` will not do anything in production because
      it's actually being loaded into environment variables by Docker for the local environment)
2. The Python equivalent in the ApplicationSettings class in this file
3. `.env.example` (good idea, so that people who clone the repo know what's needed)
"""
from pydantic import BaseSettings


class ApplicationSettings(BaseSettings):
    postgres_user: str
    postgres_password: str = ""
    postgres_db: str
    postgres_host: str = "localhost"
    postgres_port: int = 5432

    debug: bool = False

    @property
    def postgres_url(self) -> str:
        """Database connection URL"""
        return (
            f"postgresql+{% if cookiecutter.framework == "Falcon 3 (ASGI)" %}asyncpg{% else %}psycopg2{% endif %}://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}"
            f":{self.postgres_port}/{self.postgres_db}"
        )

    class Config:
        env_file = "../.env"


# Configure settings object from environment variables
settings = ApplicationSettings()
