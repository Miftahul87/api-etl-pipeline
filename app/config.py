from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    database_url: str = "sqlite:///./etl.db"
    source_api_url: str = "http://127.0.0.1:8000/mock-source"
    source_page_size: int = 10
    source_max_pages: int = 100
    http_timeout_seconds: float = 10.0
    max_retries: int = 3
    retry_backoff_seconds: float = 0.5
    model_config = SettingsConfigDict(env_file=".env",extra="ignore")
settings=Settings()
