from pydantic_settings import BaseSettings
 
class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str
    DERIBIT_BASE_URL: str
 
    class Config:
        env_file = '.env'
        # pydantic-settings reads automatically.env file
    
 
settings = Settings()
# Singleton: one object for the whole app
# Importing'settings' everywhere we need
