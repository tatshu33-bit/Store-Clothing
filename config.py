"""
Configuration settings for Store-Clothing application
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24).hex())
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'adminpass')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    WTF_CSRF_TIME_LIMIT = None  # CSRF tokens don't expire
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'db.sqlite')


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    DATABASE_PATH = ':memory:'  # Use in-memory database for tests
    WTF_CSRF_ENABLED = False  # Disable CSRF for tests


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
