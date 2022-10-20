from pydantic import BaseSettings

from app.database import Base


class Settings(BaseSettings):
    database_hostname: str
    database_port:
