import psycopg2
import logging

from psycopg2 import sql
from schema_map import get_table

log = logging.getLogger("db")

class EmployeesRepo:
    TABLE_KEYS = {"t2": "table_2", "t3": "table_3"}

    def __init__(self, connection):
        self.connection = connection
        self._n = {alias: get_table(key) for alias, key in self.TABLE_KEYS.items()}

    def add_employee (self, c_1, c_2, c_3, c_4):
        table = self._n["t3"]

        query = sql.SQL(
            """
            INSERT INTO {table}({c_1}, {c_2}, {c_3}, {c_4}) 
            VALUES (%s, %s, %s, %s)
            RETURNING {c_id};
            """
            ).format(
                table = sql.Identifier(table["table_e"]),
                c_1 = sql.Identifier(table["c_1"]),
                c_2 = sql.Identifier(table["c_2"]),
                c_3 = sql.Identifier(table["c_3"]),
                c_4 = sql.Identifier(table["c_4"]),
                c_id = sql.Identifier(table["c_id"])
                )
        try:
            with self.connection:
                with self.connection.cursor() as cur:
                    cur.execute(query, (c_1, c_2, c_3, c_4))
                    log.info("Удалось создать сотрудника")
                    return cur.fetchone()[0]
        except psycopg2.Error as error:
            log.error("не удалось создать сотрудника pgcode=%s", error.pgcode)
            raise RuntimeError("Не удалось создать сотрудника") from None

    def get_employees(self):
        table = self._n["t3"]

        query = sql.SQL(
            """
            SELECT * FROM {table};
            """
        ).format(
            table = sql.Identifier(table["table_e"])
        )
        try:
            with self.connection.cursor() as cur:
                cur.execute(query)
                log.info("Удалось получить список сотрудников")
                return cur.fetchall()
        except psycopg2.Error as error:
            log.error("не удалось получить список сотрудников pgcode=%s", error.pgcode)
            raise RuntimeError("Не удалось получить список сотрудников") from None

    def get_employee_by_id(self, c_id_3):
        table_2 = self._n["t2"]
        table_3 = self._n["t3"]

        query = sql.SQL(
            """
            SELECT e.{c_1}, e.{c_2}, r.{c_4}
            FROM {table_3} AS e
            JOIN {table_2} AS r ON r.{c_id_2}=e.{c_3}
            WHERE e.{c_id_3} = %s;
            """
            ).format(
                table_2 = sql.Identifier(table_2["table_ro"]),
                table_3 = sql.Identifier(table_3["table_e"]),
                c_1 = sql.Identifier(table_3["c_1"]),
                c_2 = sql.Identifier(table_3["c_2"]),
                c_3 = sql.Identifier(table_3["c_3"]),
                c_4 = sql.Identifier(table_2["c_1"]),
                c_id_2 = sql.Identifier(table_2["c_id"]),
                c_id_3 = sql.Identifier(table_3["c_id"])
            )
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, (c_id_3,))
                log.info("Удалось получить информацию о сотруднике")
                return cursor.fetchone()
        except psycopg2.Error as error:
            log.error("не удалось получить информацию о сотруднике pgcode=%s", error.pgcode)
            raise RuntimeError("Не удалось получить информацию о сотруднике") from None

    def get_employee_by_c1_c2(self, c_1, c_2):
        table_2 = self._n["t2"]
        table_3 = self._n["t3"]

        query = sql.SQL(
            """
            SELECT e.{c_1}, e.{c_2}, r.{c_4}, r.{c_5}
            FROM {table_3} AS e
            JOIN {table_2} AS r ON r.{c_id_2}=e.{c_3}
            WHERE e.{c_1} = %s AND e.{c_2} = %s;
            """
            ).format(
                table_2 = sql.Identifier(table_2["table_ro"]),
                table_3 = sql.Identifier(table_3["table_e"]),
                c_1 = sql.Identifier(table_3["c_1"]),
                c_2 = sql.Identifier(table_3["c_2"]),
                c_3 = sql.Identifier(table_3["c_3"]),
                c_4 = sql.Identifier(table_2["c_1"]),
                c_5 = sql.Identifier(table_2["c_2"]),
                c_id_2 = sql.Identifier(table_2["c_id"]),
            )
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, (c_1, c_2))
                log.info("Удалось получить информацию о сотруднике")
                return cursor.fetchone()
        except psycopg2.Error as error:
            log.error("не удалось получить информацию о сотруднике pgcode=%s", error.pgcode)
            raise RuntimeError("Не удалось получить информацию о сотруднике") from None

    def modify_employee_by_id(self, c_id, c_1, c_2, c_3, c_4):
        table = self._n["t3"]

        query = sql.SQL(
            """
            UPDATE {table}
            SET {c_1} = %s, {c_2} = %s, {c_3} = %s, {c_4} = %s
            WHERE {c_id} = %s;
            """
            ).format(
                table = sql.Identifier(table["table_e"]),
                c_1 = sql.Identifier(table["c_1"]),
                c_2 = sql.Identifier(table["c_2"]),
                c_3 = sql.Identifier(table["c_3"]),
                c_4 = sql.Identifier(table["c_4"]),
                c_id = sql.Identifier(table["c_id"])
                )
        try:
            with self.connection:
                with self.connection.cursor() as cursor:
                    cursor.execute(query, (c_1, c_2, c_3, c_4, c_id))
                    log.info("Удалось модифицировать информацию сотрудника")
                    return cursor.rowcount
        except psycopg2.Error as error:
            log.error("не удалось модифицировать информацию сотрудника pgcode=%s", error.pgcode)
            raise RuntimeError("Не удалось модифицировать информацию сотрудника") from None

    def modify_employee_role_by_c1_c2(self, c_1, c_2, c_3):
        table = self._n["t3"]

        query = sql.SQL(
            """
            UPDATE {table}
            SET {c_3} = %s
            WHERE {c_1} = %s AND {c_2}=%s;
            """
            ).format(
                table = sql.Identifier(table["table_e"]),
                c_1 = sql.Identifier(table["c_1"]),
                c_2 = sql.Identifier(table["c_2"]),
                c_3 = sql.Identifier(table["c_3"]),
            )
        try:
            with self.connection:
                with self.connection.cursor() as cursor:
                    cursor.execute(query, (c_3, c_1, c_2))
                    log.info("Удалось изменить роль сотрудника")
                    return cursor.rowcount
        except psycopg2.Error as error:
            log.error("не удалось изменить роль сотрудника pgcode=%s", error.pgcode)
            raise RuntimeError("Не удалось изменить роль сотрудника") from None

    def del_employee_by_id(self, c_id):
        table = self._n["t3"]

        query = sql.SQL(
            """
            DELETE FROM {table}
            WHERE {c_id} = %s;
            """
        ).format(
            table = sql.Identifier(table["table_e"]),
            c_id = sql.Identifier(table["c_id"])
            )
        try:
            with self.connection:
                with self.connection.cursor() as cursor:
                    cursor.execute(query, (c_id,))
                    log.info("Удалось удалить сотрудника")
                    return cursor.rowcount
        except psycopg2.Error as error:
            log.error("не удалось удалить сотрудника pgcode=%s", error.pgcode)
            raise RuntimeError("Не удалось удалить сотрудника") from None