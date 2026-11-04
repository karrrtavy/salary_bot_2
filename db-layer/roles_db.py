import psycopg2
import logging

from psycopg2 import sql
from schema_map import get_table

log = logging.getLogger("db")

class RoleRepo:
    TABLE_KEY = "table_2"

    def __init__(self, connection):
        self.connection = connection
        self._n = get_table(self.TABLE_KEY)

    def get_all(self):
        n = self._n

        query = sql.SQL(
            """
            SELECT * FROM {table};
            """
            ).format(
            table = sql.Identifier("table_ro")
            )
        try:
            with self.connection.cursor() as cur:
                cur.execute(query)
                log.info("Удалось получить данные из таблицы")
                return cur.fetchall()
        except psycopg2.Error as error:
            log.error("не удалось получить данные из таблицы pgcode=%s", error.pgcode)
            raise RuntimeError("Не удалось получить данные из таблицы") from None

    def get_by_name(self, name):
        n = self._n

        query = sql.SQL(
            """
            SELECT {c_id}, {c1}, {c2} 
            FROM {table} 
            WHERE {c1} = %s;
            """
            ).format(
            c_id = sql.Identifier("c_id"),
            c1 = sql.Identifier("c1"),
            c2 = sql.Identifier("c2"),
            table = sql.Identifier("table_ro")
            )
        try:
            with self.connection.cursor() as cur:
                cur.execute(query, (name,))
                log.info("Удалось получить данные из таблицы")
                return cur.fetchone()
        except psycopg2.Error as error:
            log.error("не удалось получить данные из таблицы pgcode=%s", error.pgcode)
            raise RuntimeError("Не удалось получить данные из таблицы") from None