# -*- coding: utf-8 -*-
"""
@Time    : 2022/8/18 23:42
@Author  : itlubber
@Site    : itlubber.art
"""

import traceback
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.dialects.sqlite import INTEGER, VARCHAR, FLOAT

import impala.dbapi as creater
from impala.util import as_pandas
from contextlib import contextmanager

from .pooled_db import PooledDB


__all__ = ["HiveConnectPool"]


class HiveConnectPoolQuery:

    def __init__(self, conn, cursor):
        self.conn = conn
        self.cursor = cursor

    def close(self):
        self.conn.close()
        self.cursor.close()


class HiveConnectPool:

    def __init__(self, **kwargs):
        self._pool = PooledDB(creater, **kwargs)

    @contextmanager
    def register_hive_connect_query(self):
        try:
            _conn = self._pool.connection()
            _cursor = _conn.cursor()
            _query = HiveConnectPoolQuery(_conn, _cursor)
            yield _query
        except Exception as error:
            print(traceback.format_exc())
        finally:
            _query.close()

    def query(self, query, result=None, index=None):
        with self.register_hive_connect_query() as _hive_connect_query:
            _hive_connect_query.cursor.execute(query)
            if index:
                _data = as_pandas(_hive_connect_query.cursor)
                if index not in _data.columns:
                    raise "index must in the result set's schema."
                else:
                    if result is None or result != "record":
                        return {group_name: group.drop(columns=[index]).to_dict(orient="record")[0] for group_name, group in _data.groupby(index)}
                    else:
                        return {group_name: group.drop(columns=[index]).to_dict(orient="record") for group_name, group in _data.groupby(index)}

            if result == "data":
                return as_pandas(_hive_connect_query.cursor)
            elif result == "record":
                column_names = [col[0] for col in _hive_connect_query.cursor.description]
                return [dict(zip(column_names, row)) for row in _hive_connect_query.cursor.fetchall()]
            else:
                return _hive_connect_query.cursor.fetchall()

    def execute(self, query, params=None):
        with self.register_hive_connect_query() as _hive_connect_query:
            try:
                if params:
                    _hive_connect_query.cursor.execute(query, params)
                else:
                    _hive_connect_query.cursor.execute(query)
                _hive_connect_query.conn.commit()
            except Exception as error:
                _hive_connect_query.conn.rollback()
                traceback.print_exc()
                raise Exception("sql语句执行失败")
    
    @staticmethod
    def data_type_dict(data: pd.DataFrame):
        type_dict = {}
        for col in data.columns:
            tp = data[col].dtype
            if 'object' in str(tp):
                type_dict[col] = VARCHAR()
                data[col] = data[col].apply(lambda x: str(x))
            elif 'int' in str(tp):
                type_dict[col] = INTEGER()
            elif 'float' in str(tp):
                type_dict[col] = FLOAT()
            else:
                type_dict[col] = VARCHAR()
        return type_dict

    def to_impala(self, data: pd.DataFrame, table_name="features_tables", if_exists="replace", index=False, chunksize=1024, *args, **kwargs):
        engine = create_engine(*args, **kwargs)
        data.to_sql(table_name, con=engine, if_exists=if_exists, index=index, dtype=self.data_type_dict(data), chunksize=chunksize)
