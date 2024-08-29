# app/config.py

class Config:
    """Base configuration."""
    SECRET_KEY = 'weborder'

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'root'
    MYSQL_DB = 'weborder'
    MYSQL_CURSORCLASS = 'DictCursor'  # 可选，返回字典而不是元组

class ProductionConfig(Config):
    """Production configuration."""
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'your_username'
    MYSQL_PASSWORD = 'your_password'
    MYSQL_DB = 'your_production_database_name'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
