from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "tasks-service"
    DATABASE_URL: str = "postgresql://postgres:admin@localhost:5432/project_db"

    class Config:
        env_file = ".env"

settings = Settings()
