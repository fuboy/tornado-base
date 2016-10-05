from .config import DevelopmentConfig


class MyConfig(DevelopmentConfig):
    db_uri = 'postgresql+psycopg2://test:test@localhost:5432/database'
