import psycopg2
import logging

from schema_map import get_table
from psycopg2 import sql

log = logging.getLogger("db")

class ES_Repo:
    TABLES_KEYS = {"t3": "table_3", "t4": "table_4", "t5": "table_5"}

    def __init__(self, connection):
        self.connection = connection
        self._n = {alias: get_table(key) for alias, key in self.TABLES_KEYS.items()}

    def create_employee_shift_by_employee_c1_c2(self, c_1, c_2, e_c_1, e_c_2, ss_c_1):
        table_3 = self._n["t3"]
        table_4 = self._n["t4"]
        table_5 = self._n["t5"]

        query = sql.SQL(
            """
            INSERT INTO {table_5}({c_1}, {c_2}, {c_3}, {c_4})
            VALUES (
                %s, %s,
                (SELECT {es_c_id} FROM {table_3} WHERE {es_c_1} = %s AND {es_c_2} = %s),
                (SELECT {ss_c_id} FROM {table_4} WHERE {ss_c_1} = %s)
            )
            RETURNING {c_id};
            """
            ).format(
                table_3 = sql.Identifier(table_3["table_e"]),
                table_4 = sql.Identifier(table_4["table_ss"]),
                table_5 = sql.Identifier(table_5["table_es"]),
                c_1 = sql.Identifier(table_5["c_1"]),
                c_2 = sql.Identifier(table_5["c_2"]),
                c_3 = sql.Identifier(table_5["c_3"]),
                c_4 = sql.Identifier(table_5["c_4"]),
                es_c_id = sql.Identifier(table_3["c_id"]),
                es_c_1 = sql.Identifier(table_3["c_1"]),
                es_c_2 = sql.Identifier(table_3["c_2"]),
                ss_c_id = sql.Identifier(table_4["c_id"]),
                ss_c_1 = sql.Identifier(table_4["c_1"]),
                c_id = sql.Identifier(table_5["c_id"])
            )
        try:
            with self.connection:
                with self.connection.cursor() as cur:
                    cur.execute(query, (c_1, c_2, e_c_1, e_c_2, ss_c_1))
                    log.info("Удалось создать смену сотрудника")
                    return cur.fetchone()
        except psycopg2.Error as error:
            log.error("не удалось создать смену сотрудника psycopg=%s", error.pgcode)
            raise RuntimeError("не удалось создать смену сотрудника") from None

    def get_employee_shifts(self):
        table_5 = self._n["t5"]

        query = sql.SQL(
            """
            SELECT * FROM {table};
            """
            ).format(
                table = sql.Identifier(table_5["table_es"])
            )
        try:
            with self.connection.cursor() as cur:
                cur.execute(query)
                log.info("Удалось получить данные из таблицы")
                return cur.fetchall()
        except psycopg2.Error as error:
            log.error("не удалось получить данные из таблицы psycopg=%s", error.pgcode)
            raise RuntimeError("не удалось получить данные из таблицы") from None

    def get_employee_shifts_by_employee_c1_c2(self, e_c_1, e_c_2):
        table_3 = self._n["t3"]
        table_4 = self._n["t4"]
        table_5 = self._n["t5"]

        query = sql.SQL(
            """
            SELECT es.*
            FROM {table_5} AS es
            JOIN {table_3} as e ON e.{c_id} = es.{c_3}
            WHERE e.{c_1} = %s AND e.{c_2} = %s;
            ORDER BY {table_4}.{ss_c_1} DESC;
            """    
            ).format(
                table_5 = sql.Identifier(table_5["table_es"]),
                table_3 = sql.Identifier(table_3["table_e"]),
                c_id = sql.Identifier(table_3["c_id"]),
                c_3 = sql.Identifier(table_5["c_3"]),
                c_1 = sql.Identifier(table_3["c_1"]),
                c_2 = sql.Identifier(table_3["c_2"]),
                table_4 = sql.Identifier(table_4["table_ss"]),
                ss_c_1 = sql.Identifier(table_4["c_1"])
            )
        try:
            with self.connection.cursor() as cur:
                cur.execute(query, (e_c_1, e_c_2))
                log.info("Удалось получить данные из таблицы")
                return cur.fetchall()
        except psycopg2.Error as error:
            log.error("не удалось получить данные из таблицы psycopg=%s", error.pgcode)
            raise RuntimeError("не удалось получить данные из таблицы") from None

    def get_shift_by_date(self):
        table_4 = self._n["t4"]
        table_5 = self._n["t5"]

        query = sql.SQL(
            """
            SELECT es.*
            FROM {table_5} AS es
            JOIN {table_4} as ss ON ss.{c_id} = es.{c_4}
            WHERE ss.{c_1} = %s;
            """
            ).format(
                table_5 = sql.Identifier(table_5["table_es"]),
                table_4 = sql.Identifier(table_4["table_ss"]),
                c_id = sql.Identifier(table_4["c_id"]),
                c_4 = sql.Identifier(table_5["c_4"]),
                c_1 = sql.Identifier(table_4["c_1"])
            )
        try:
            with self.connection.cursor() as cur:
                cur.execute(query, (ss_c_1,))
                log.info("Удалось получить данные из таблицы")
                return cur.fetchall()
        except psycopg2.Error as error:
            log.error("не удалось получить данные из таблицы psycopg=%s", error.pgcode)
            raise RuntimeError("не удалось получить данные из таблицы") from None