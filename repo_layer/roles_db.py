import psycopg2
import logging

from psycopg2 import sql

from schema_map import get_table
from models.role import Role

log = logging.getLogger("db")

class RoleRepo:
    def __init__(self, connection):
        self.connection = connection
        self._n = get_table(Role.TABLE_KEY)

    @staticmethod
    def to_model(row) -> Role:
        return Role(c_id=row[0], c_1=row[1], c_2=row[2])

    def select(self) -> sql.Composed:
        n = self._n
        return sql.SQL(
            """
            SELECT {c_id}, {c_1}, {c_2} FROM {table} 
            """
            ).format(
                c_id = sql.Identifier(n["c_id"]),
                c_1 = sql.Identifier(n["c_1"]),
                c_2 = sql.Identifier(n["c_2"]),
                table = sql.Identifier(n["table_ro"])
            )

    def get_all(self):
        query = self.select()
        try:
            with self.connection.cursor() as cur:
                cur.execute(query)
                log.info("Удалось получить данные из таблицы")
                rows = cur.fetchall()
                return [self.to_model(row) for row in rows]
        except psycopg2.Error as error:
            self.connection.rollback()
            log.error("не удалось получить данные из таблицы pgcode=%s", error.pgcode)
            raise RuntimeError("Не удалось получить данные из таблицы") from None

    def get_by_name(self, name: str):
        query = self.select() + sql.SQL("WHERE {c_1} = %s;").format(
            c_1 = sql.Identifier(self._n["c_1"])
        )
        try:
            with self.connection.cursor() as cur:
                cur.execute(query, (name,))
                log.info("Удалось получить данные из таблицы")
                row = cur.fetchone()
                return self.to_model(row) if row else None
        except psycopg2.Error as error:
            self.connection.rollback()
            log.error("не удалось получить данные из таблицы pgcode=%s", error.pgcode)
            raise RuntimeError("Не удалось получить данные из таблицы") from None