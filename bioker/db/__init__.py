from typing import List

from pandas import read_sql, DataFrame
from sqlalchemy import create_engine as ce, MetaData
from sqlalchemy.engine import Engine
from sqlalchemy.ext.automap import automap_base as ab, AutomapBase
from sqlalchemy.orm import Session


def create_mysql_url(user: str = 'root', pwd: str = '', host: str = 'mysql',
                     port: str = '3306', db: str = 'test') -> str:
    return 'mysql+pymysql://{}:{}@{}:{}/{}'.format(user, pwd, host, port, db)


def create_engine(url: str) -> Engine:
    return ce(url)


def automap_base(engine: Engine) -> AutomapBase:
    base = ab()
    base.prepare(engine, reflect=True)
    return base


def automap_meta(engine: Engine) -> MetaData:
    meta = MetaData()
    meta.reflect(engine)
    return meta


def session(engine: Engine) -> Session:
    return Session(engine)


def pd_read_sql_file(engine: Engine, path: str, params: dict = None) -> DataFrame:
    with open(path, 'r') as f:
        sql = f.read()
    return pd_read_sql(engine, sql, params=params)


def pd_read_sql(engine: Engine, sql: str, params=None) -> DataFrame:
    return read_sql(sql, engine, params=params)


def get_tables(engine: Engine) -> List[str]:
    meta = automap_meta(engine)
    return meta.tables.keys()


def get_columns(engine: Engine, table_name: str) -> List[str]:
    meta = automap_meta(engine)
    return [column.name for column in meta.tables[table_name].columns]
