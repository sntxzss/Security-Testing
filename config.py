from pydantic_settings import BaseSettings, SettingsConfigDict

class Setting(BaseSettings):
    jwt_secret:str
    jwt_algorithm: str = "HS256"
    access_token_minutes: int = 30

    model_config = SettingsConfigDict(env_file=".env", env_prefix="")

settings = Setting()