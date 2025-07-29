from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):    
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_USERNAME: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    MATRIX_SERVER: str
    APP_MODE: str
    BRIDGE_TELEGRAM_URL: str
    BRIDGE_TELEGRAM_SHARED_SECRET: str
    BRIDGE_WHITE_LISTED_URL: str

    @property
    def database_url(self):
        return f"postgresql://{self.POSTGRES_USERNAME}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


settings = Settings()