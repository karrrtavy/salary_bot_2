import psycopg2
import logging

from schema_map import get_table
from psycopg2 import sql
from models.schedule_shift import Schedule

log = logging.getLogger("db")

class SSRepo:
    def __init__(self, connection):
        self.connection = connection
        self._n = get_table(Schedule.TABLE_KEY)

    def to_model(row) -> Schedule:
        return Schedule(c_id = row[0], c_1 = row[1], c_2 = row[2])

    def create_shift(self, c_1, c_2):
        n = self._n

        query = sql.SQL(
            """
            INSERT INTO {table}({c_1}, {c_2})
            VALUES (%s, %s) 
            RETURNING {c_id};
            """
            ).format(
                table = sql.Identifier(n["table_ss"]),
                c_1 = sql.Identifier(n["c_1"]),
                c_2 = sql.Identifier(n["c_2"]),
                c_id = sql.Identifier(n["c_id"])
            )
        try:
            with self.connection:
                with self.connection.cursor() as cur:
                    cur.execute(query, (c_1, c_2))
                    log.info("удалось создать смену")
                    return cur.fetchone()
        except psycopg2.Error as error:
            log.error("не удалось создать смену psycopg=%s", error.pgcode)
            raise RuntimeError("не удалось создать смену") from None

    def get_shifts(self):
        n = self._n

        query = sql.SQL(
            """
            SELECT * FROM {table};
            """
            ).format(
                table = sql.Identifier(n["table_ss"])
            )
        try:
            with self.connection.cursor() as cur:
                cur.execute(query)
                log.info("Удалось получить данные из таблицы")
                return cur.fetchall()
        except psycopg2.Error as error:
            log.error("не удалось получить данные из таблицы psycopg=%s", error.pgcode)
            raise RuntimeError("не удалось получить данные из таблицы") from None
        
    def get_shift_by_date(self, c_1):
        n = self._n

        query = sql.SQL(
            """
            SELECT * FROM {table} WHERE {c_1} = %s;
            """
            ).format(
                table = sql.Identifier(n["table_ss"]),
                c_1 = sql.Identifier(n["c_1"])
            )
        try:
            with self.connection.cursor() as cur:
                cur.execute(query, (c_1, ))
                log.info("удалось получить данные из таблицы по дате")
                return cur.fetchall()
        except psycopg2.Error as error:
            log.error("не удалось получить данные из таблицы по дате psycopg=%s", error.pgcode)
            raise RuntimeError("не удалось получить данные из таблицы по дате") from None