from .core.config import Config


class DevelopmentConfig(Config):
    debug = True
    autoreload = True


class DeploymentConfig(Config):
    debug = False
    autoreload = False
    autoescape = None

    xsrf_cookies = True
    compiled_template_cache = True

    host = '127.0.0.1'

    db_uri = 'postgresql+psycopg2://test:test@localhost:5432/database'

    cookie_secret = '__TODO_SOMETHING__'
    xsrf_cookies = True

    compiled_template_cache = True
    static_hash_cache = True


class TestConfig(Config):
    debug = True
    autoreload = True