from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "mysql+pymysql://root:1234@localhost:3306/blood_bank_db"

    class Config:
        env_file = ".env"


settings = Settings()
