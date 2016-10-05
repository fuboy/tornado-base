from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from project.core.basehandler import t_url
from project.core.db import db
from project.core.scope import scope
from project.core.application import Application
from project.utils.tor_dict import obj_to_dict


def make_app(config):
    routes = retrieve_routes(config)
    app = Application(routes, **obj_to_dict(config))

    sqlalchemy_config(app)

    return app


def retrieve_routes(config):
    routes = []
    for m_desc, m_name in config.modules.items():
        module = __import__('project.modules.{module_name}.handlers'.format(module_name=m_name), fromlist=['handlers'])

        routes += module.routes

    return routes


def sqlalchemy_config(app):
    engine = create_engine(app.settings.get('db_uri'), convert_unicode=True)
    db_session = scoped_session(sessionmaker(autocommit=False,
                                             expire_on_commit=False,
                                             autoflush=False,
                                             bind=engine),
                                scopefunc=scope.get())

    db.engine  = db.BaseModel.engine  = engine
    db.session = db.BaseModel.session = db_session
    db.query   = db.BaseModel.query   = db_session.query_property()