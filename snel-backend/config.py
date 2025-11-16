import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration de base"""
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://snel_user:motdepasse@localhost/snel_payroll"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
    JSON_SORT_KEYS = False


class DevelopmentConfig(Config):
    """Configuration développement"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Configuration production"""
    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """Configuration tests"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig
}
