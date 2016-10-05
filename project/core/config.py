import os
from . import uimodules

from .errorhandler import ErrorHandler


class Config(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Config, cls).__new__(cls, *args, **kwargs)

        return cls._instance

    host = '0.0.0.0'
    port = '8080'

    db_uri = 'postgresql+psycopg2://test:test@localhost:5432/database'

    user_types = [
        'admin',
        'client',
    ]

    debug = False
    autoreload = False
    autoescape = None

    token_secret_key = '___TODO_SOMETHING__'
    token_pass_salt = '__TODO_SOMETHING___'

    cookie_secret = '__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__'
    xsrf_cookies = False

    jwt_secret = '__TODO:__GENERATE_HARD_PHRASE_IN_PRODUCTION__'
    jwt_algorithm = 'HS256'

    login_url = '/auth/login/'
    logout_url = '/auth/logout/'

    static_path = os.path.join(os.path.dirname(__file__), '../static')
    template_path = os.path.join(os.path.dirname(__file__), '../templates')

    compiled_template_cache = False  # True
    static_hash_cache = False
    serve_traceback = True

    default_handler_class = ErrorHandler
    default_handler_args = dict(status_code=404)

    template_403 = 'errors/403.html'
    template_404 = 'errors/404.html'
    template_500 = 'errors/500.html'
    template_xxx = 'errors/xxx.html'

    modules = {
        'Auth Module': 'auth',
        'User Module': 'user',
        'Admin Module': 'user.admin',
        'Client Module': 'user.client',
        'Log Module': 'log',
    }

    socket_app = False

    mail_smtp = {
        'host': 'smtp.gmail.com',
        'port': 587,
        'username': 'test@gmail.com',
        'password': 'somethings',
        'use_tls': None,
        'fail_silently': False
    }

    ui_modules = uimodules

    # redis session cache
    pycket = {
        'engine': 'redis',
        'storage': {
            'host': 'localhost',
            'port': 6379,
            'db_sessions': 10,
            'db_notifications': 11,
            'max_connections': 2 ** 31,
        },
        'cookies': {
            # 'expires': 1,
        },
    }

    # OAuth2 configs
    google_oauth = {
        'key': 'temp',
        'secret': 'temp',
        'redirect_url': 'http://127.0.0.1:8080/auth/google',
        'scope': ['profile', 'email']  # TODO Check and extend
    }

    instagram_oauth = {
        'client_id': 'temp',
        'client_secret': 'temp',
        'redirect_uri': 'http://127.0.0.1:8080/auth/instagram/',
        'scopes': 'basic public_content'
    }