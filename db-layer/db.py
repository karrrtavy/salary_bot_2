import os
import psycopg2
import logging

from pathlib import Path
from dotenv import load_dotenv
from psycopg2 import pool

load_dotenv()

log = logging.getLogger("db")
_db_pool = None

def get_pool():
    global _db_pool

    if _db_pool is None:
        _db_pool = pool.SimpleConnectionPool(
            minconn=1,
            maxconn=10,
            dbname = os.getenv("DBNAME"),
            user = os.getenv("DBUSER"),
            password = os.getenv("DBPASSWORD"),
            host = os.getenv("DBHOST"),
            port = os.getenv("DBPORT")
            )
    return _db_pool

def close_pool():
    global _db_pool

    if _db_pool is not None:
        _db_pool.closeall()
        _db_pool = None

def load_schema() -> str:
    path = os.getenv("SCHEMA_PATH")
    
    if not path:
        raise RuntimeError("путь к схеме не указан")
    try:
        return Path(path).read_text(encoding="utf-8")
    except OSError:
        raise RuntimeError("не удалось прочитать схемы") from None

class Database:
    def __init__(self):
        self.connection = None
        try:
            self.connection = get_pool().getconn()
        except (psycopg2.Error, pool.PoolError):
            raise RuntimeError("Не удалось подключиться к БД") from None
        
        try:
            with self.connection.cursor() as cur:
                cur.execute(load_schema())
            self.connection.commit()
        except (psycopg2.Error, RuntimeError) as error:
            self.connection.rollback()
            get_pool().putconn(self.connection)
            self.connection = None
            if isinstance(error, psycopg2.Error):
                log.error("ошибка схемы БД pgcode=%s", error.pgcode)
            raise RuntimeError("Не удалось создать таблицы БД") from None

    def close(self):
        if self.connection is not None:
            self.connection.rollback()
            get_pool().putconn(self.connection)
            self.connection = None

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()