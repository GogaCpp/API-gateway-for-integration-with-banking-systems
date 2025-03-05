from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = ConfigDict(extra='ignore')

    # Database
    db_host: str
    db_port: int
    db_user: str
    db_password: str
    db_name: str

    @property
    def db_url(self):
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

settings = Settings(
    _env_file=".env",
    _env_file_encoding="utf-8"
)
