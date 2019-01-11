from sqlalchemy.ext.automap import automap_base as ab
from sqlalchemy import create_engine as ce, MetaData
from sqlalchemy.orm import Session

def create_engine(url):
    """Creates SQLAlchemy engine by passed url
    Parameters:
    url - engine url
    """
    return ce(url)

def automap_base(engine):
    """Creates SQLAlchemy Base reflected with engine
    Parameters:
    engine - SQLAlchemy engine
    """
    Base = ab()
    Base.prepare(engine, reflect=True)
    return Base

def automap_meta(engine):
    """Creates SQLAlchemy MetaData reflected with engine
    Parameters:
    engine - SQLAlchemy engine
    """
    meta = MetaData()
    meta.reflect(engine)
    return meta

def session(engine):
    """Creates SQLAlchemy session
    Parameters:
    engine - SQLAlchemy engine
    """
    return Session(engine)
