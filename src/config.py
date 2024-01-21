import os
from typing import Literal

from dotenv import load_dotenv

load_dotenv()


class Settings:

    MODE : Literal["DEV", "TEST", "PROD"] = os.getenv("MODE")
    LOG_LEVEL : Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = os.getenv("LOG_LEVEL")

    DB_HOST : str = os.getenv("DB_HOST")
    DB_PORT : int = os.getenv("DB_PORT")
    DB_NAME : str = os.getenv("DB_NAME")
    DB_USER : str = os.getenv("DB_USER")
    DB_PASS : str = os.getenv("DB_PASS")
    
    @property
    def DB_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


    TEST_DB_HOST : str = os.getenv("TEST_DB_HOST")
    TEST_DB_PORT : int = os.getenv("TEST_DB_PORT")
    TEST_DB_NAME : str = os.getenv("TEST_DB_NAME")
    TEST_DB_USER : str = os.getenv("TEST_DB_USER")
    TEST_DB_PASS : str = os.getenv("TEST_DB_PASS")

    @property
    def TEST_DB_URL(self):
        return f"postgresql+asyncpg://{self.TEST_DB_USER}:{self.TEST_DB_PASS}@{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}"


    REDIS_HOST : str = os.getenv("REDIS_HOST")
    REDIS_PORT : int = os.getenv("REDIS_PORT")
    REDIS_DB : int = os.getenv("REDIS_DB")
    
    @property
    def REDIS_URL(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"


    SMTP_HOST: str = os.getenv("SMTP_HOST")
    SMTP_PORT: int = os.getenv("SMTP_PORT")
    SMTP_USER: str = os.getenv("SMTP_USER")
    SMTP_PASS: str = os.getenv("SMTP_PASS")


    SECRET : str = os.getenv("SECRET")
    ALGORITHM : str = os.getenv("ALGORITHM")
   

settings = Settings()


