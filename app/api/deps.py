import pymysql
from injector import Module, singleton, provider
from core.db import get_db_connection


class MySQLModule(Module):
    # @singleton
    # @provider
    def data_base_connection(self) -> pymysql.connections.Connection:
        return get_db_connection()
