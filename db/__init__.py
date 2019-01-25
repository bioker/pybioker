from sqlalchemy.ext.automap import automap_base as ab
from sqlalchemy import create_engine as ce, MetaData
from sqlalchemy.orm import Session

def create_engine(url):
    """Creates SQLAlchemy engine by passed url

    :param url - engine url

    :type url: str

    :rtype: sqlalchemy.engine.Engine
    """
    return ce(url)

def automap_base(engine):
    """Creates SQLAlchemy Base reflected with engine

    :param engine - SQLAlchemy engine

    :type engine: sqlalchemy.engine.Engine

    :rtype: sqlalchemy.ext.automap.AutomapBase
    """
    Base = ab()
    Base.prepare(engine, reflect=True)
    return Base

def automap_meta(engine):
    """Creates SQLAlchemy MetaData reflected with engine

    :param engine - SQLAlchemy engine

    :type engine: sqlalchemy.engine.Engine

    :rtype: sqlalchemy.MetaData
    """
    meta = MetaData()
    meta.reflect(engine)
    return meta

def session(engine):
    """Creates SQLAlchemy session

    :param engine - SQLAlchemy engine

    :type engine: sqlalchemy.engine.Engine

    :rtype: sqlalchemy.orm.Session
    """
    return Session(engine)
