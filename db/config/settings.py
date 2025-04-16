from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mongo_uri: str
    db_name: str
    collection_name: str
    
    class Config:
        env_file = ".env"

settings = Settings()