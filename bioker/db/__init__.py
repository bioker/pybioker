import pandas
import sqlalchemy
from pandas import read_sql
from sqlalchemy import create_engine as ce, MetaData
from sqlalchemy.ext.automap import automap_base as ab
from sqlalchemy.orm import Session


def create_mysql_url(user: str = 'root', pwd: str = '', host: str = '', port: str = '', db: str = '') -> str:
    return 'mysql+pymysql://{}:{}@{}:{}/{}'.format(user, pwd, host, port, db)


def create_engine(url: str) -> sqlalchemy.engine.Engine:
    return ce(url)


def automap_base(engine: sqlalchemy.engine.Engine) -> sqlalchemy.ext.automap.AutomapBase:
    base = ab()
    base.prepare(engine, reflect=True)
    return base


def automap_meta(engine: sqlalchemy.engine.Engine) -> sqlalchemy.MetaData:
    meta = MetaData()
    meta.reflect(engine)
    return meta


def session(engine: sqlalchemy.engine.Engine) -> sqlalchemy.orm.Session:
    return Session(engine)


def pd_read_sql_file(engine: sqlalchemy.engine.Engine, path: str, params: dict = None) -> pandas.core.frame.DataFrame:
    with open(path, 'r') as f:
        sql = f.read()
    return pd_read_sql(engine, sql, params=params)


def pd_read_sql(engine: sqlalchemy.engine.Engine, sql: str, params=None) -> pandas.core.frame.DataFrame:
    return read_sql(sql, engine, params=params)


def get_tables(engine: sqlalchemy.engine.Engine):
    meta = automap_meta(engine)
    return meta.tables.keys()


def get_columns(engine: sqlalchemy.engine.Engine, table_name: str):
    meta = automap_meta(engine)
    return list(map(lambda column: column.name, meta.tables[table_name].columns))
