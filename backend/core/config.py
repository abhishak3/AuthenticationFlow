from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
  DB_HOST: str
  DB_PORT: str
  DB_NAME: str
  DB_USER: str
  DB_PASSWORD: str

  JWT_SECRET: str
  JWT_ALGORITHM: str
  JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int
  JWT_REFRESH_TOKEN_EXPIRE_DAYS: int

  model_config = SettingsConfigDict(env_file='.env')

settings = Settings()
