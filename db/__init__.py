from pandas import read_sql
from sqlalchemy.ext.automap import automap_base as ab
from sqlalchemy import create_engine as ce, MetaData
from sqlalchemy.orm import Session

def create_mysql_url(user='root', pwd='', host='', port='', db=''):
    """Creates SQLAlchemy engine URL

    :type user: str
    :type pwd: str
    :type host: str
    :type port: str
    :type db: str

    :rtype: str
    """
    return 'mysql+pymysql://{}:{}@{}:{}/{}'.format(user, pwd, host, port, db)

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

def pd_read_sql_file(engine, path, params={}):
    """Creates SQLAlchemy session

    :param engine - SQLAlchemy engine
    :param path - path to file
    :param params - params to inject into query

    :type engine: sqlalchemy.engine.Engine
    :type path: str
    :type params: dict

    :rtype: pandas.core.frame.DataFrame
    """
    sql = ""
    with open(path, 'r') as f:
        sql = f.read()
    return pd_read_sql(engine, sql, params=params)

def pd_read_sql(engine, sql, params={}):
    """Creates SQLAlchemy session

    :param engine - SQLAlchemy engine
    :param sql - SQL query
    :param params - params to inject into query

    :type engine: sqlalchemy.engine.Engine
    :type sql: str
    :type params: dict

    :rtype: pandas.core.frame.DataFrame
    """
    return read_sql(sql, engine, params=params)
