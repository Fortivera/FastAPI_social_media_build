from pydantic import BaseSettings

from app.database import Base


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password
    database_name
    database_username
    secret_key
