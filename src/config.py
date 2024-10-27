from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = 'FastAPI + GPT'

    OPENAI_API_KEY: str
    GPT_MODEL: str

    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_USER: str
    DB_PASS: str

    JWT_SECRET: str
    VERIFICATION_SECRET: str

    class Config:
        env_file = '.env'

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()