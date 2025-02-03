from pydantic_settings import BaseSettings, SettingsConfigDict



class Settings(BaseSettings):
     postgres: str
     jwt_alg: str
     jwt_secret: str
     email: str
     email_password: str
     
     model_config = SettingsConfigDict(env_file=".env")
     
settings = Settings()