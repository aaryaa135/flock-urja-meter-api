from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PORTAL_BASE_URL: str = "https://urja-ops.flockenergy.tech"
    PORTAL_USERNAME: str = ""
    PORTAL_PASSWORD: str = ""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()