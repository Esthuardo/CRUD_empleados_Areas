from os import getenv
from datetime import timedelta


class BaseConfig:
    SQLALCHEMY_DATABASE_URI = getenv("DATABASE_URI")
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False
    JWT_SECRET_KEY = getenv("SECRET_KEY")


class DevelopmentConfig(BaseConfig):
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=5)


environment = {"development": DevelopmentConfig}
