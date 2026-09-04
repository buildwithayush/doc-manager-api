from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL:str=""
    TEST_DATABASE_URL:str=""
    SECRET_KEY:str ="secret_key"
    ALGORITHM: str="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES:int=60

    MINIO_ENDPOINT: str = ""
    MINIO_ACCESS_KEY: str = ""
    MINIO_SECRET_KEY: str = ""
    MINIO_BUCKET_NAME: str = "documents"
    MINIO_SECURE: bool = False

    model_config = SettingsConfigDict(env_file = '.env',extra='ignore')

settings = Settings()    