import psycopg2
import logging

from psycopg2 import sql
from schema_map import get_table

from models.employee import Employee
from models.role import Role

log = logging.getLogger("db")

class EmployeesRepo:
    def __init__(self, connection):
        self.connection = connection
        self._n = get_table(Employee.TABLE_KEY)

    def to_model(row) -> Employee:
        return Employee(c_id = row[0], c_1 = row[1], c_2 = row[2], c_3 = row[3], c_4 = row[4], c_5 = row[5])

    def registration_employee (self, c_1: str, c_2: str, c_3: int, c_4: int):
        n = self._n

        query = sql.SQL(
            """
            INSERT INTO {table}({c_1}, {c_2}, {c_3}, {c_4}) 
            VALUES (%s, %s, %s, %s)
            RETURNING {c_id};
            """
            ).format(
                table = sql.Identifier(n["table_e"]),
                c_1 = sql.Identifier(n["c_1"]),
                c_2 = sql.Identifier(n["c_2"]),
                c_3 = sql.Identifier(n["c_3"]),
                c_4 = sql.Identifier(n["c_4"]),
                c_id = sql.Identifier(n["c_id"])
                )
        try:
            with self.connection:
                with self.connection.cursor() as cur:
                    cur.execute(query, (c_1, c_2, c_3, c_4,))
                    log.info("Удалось создать сотрудника")
                    return cur.fetchone()
        except psycopg2.Error as error:
            log.error("не удалось создать сотрудника pgcode=%s", error.pgcode)
            raise RuntimeError("Не удалось создать сотрудника") from None

    def get_employees(self):
        n = self._n

        query = sql.SQL(
            """
            SELECT * FROM {table};
            """
        ).format(
            table = sql.Identifier(n["table_e"])
        )
        print(type(self.connection))
        print(hasattr(self.connection, "cursor"))
        try:
            with self.connection.cursor() as cur:
                cur.execute(query)
                log.info("Удалось получить список сотрудников")
                return cur.fetchall()
        except psycopg2.Error as error:
            self.connection.rollback()
            log.error("не удалось получить список сотрудников pgcode=%s", error.pgcode)
            raise RuntimeError("Не удалось получить список сотрудников") from None

    def get_employee_by_id(self, c_id):
        n = self._n
        n2 = get_table(Role.TABLE_KEY)

        query = sql.SQL(
            """
            SELECT e.{c_1}, e.{c_2}, e.{c_3}, r.{rc_1}, r.{rc_2}
            FROM {table} AS e
            JOIN {table_2} AS r
            ON r.{rc_id} = e.{c_4}
            WHERE e.{c_id} = %s;
            """
            ).format(
                c_1 = sql.Identifier(n["c_1"]),
                c_2 = sql.Identifier(n["c_2"]),
                c_3 = sql.Identifier(n["c_3"]),
                c_4 = sql.Identifier(n["c_4"]),
                rc_1 = sql.Identifier(n2["c_1"]),
                rc_2 = sql.Identifier(n2["c_2"]),
                table = sql.Identifier(n["table_e"]),
                table_2 = sql.Identifier(n2["table_ro"]),
                rc_id = sql.Identifier(n2["c_id"]),
                c_id = sql.Identifier(n["c_id"]),
            )
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, (c_id,))
                log.info("Удалось получить информацию о сотруднике")
                return cursor.fetchone()
        except psycopg2.Error as error:
            log.error("не удалось получить информацию о сотруднике pgcode=%s", error.pgcode)
            raise RuntimeError("Не удалось получить информацию о сотруднике") from None

    def get_employee_by_c1_c2(self, c_1, c_2):
        n = self._n
        n2 = get_table(Role.TABLE_KEY)

        query = sql.SQL(
            """
            SELECT e.{c_1}, e.{c_2}, r.{c_4}, r.{c_5}
            FROM {table_3} AS e
            JOIN {table_2} AS r ON r.{c_id_2}=e.{c_3}
            WHERE e.{c_1} = %s AND e.{c_2} = %s;
            """
            ).format(
                table_2 = sql.Identifier(n2["table_ro"]),
                table_3 = sql.Identifier(n["table_e"]),
                c_1 = sql.Identifier(n["c_1"]),
                c_2 = sql.Identifier(n["c_2"]),
                c_3 = sql.Identifier(n["c_3"]),
                c_4 = sql.Identifier(n2["c_1"]),
                c_5 = sql.Identifier(n2["c_2"]),
                c_id_2 = sql.Identifier(n2["c_id"]),
            )
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, (c_1, c_2))
                log.info("Удалось получить информацию о сотруднике")
                return cursor.fetchone()
        except psycopg2.Error as error:
            log.error("не удалось получить информацию о сотруднике pgcode=%s", error.pgcode)
            raise RuntimeError("Не удалось получить информацию о сотруднике") from None

    def modify_employee_by_id(self, c_id, c_1, c_2, c_4, c_5):
        n = self._n

        query = sql.SQL(
            """
            UPDATE {table}
            SET {c_1} = %s, {c_2} = %s, {c_4} = %s, {c_5} = %s
            WHERE {c_id} = %s;
            """
            ).format(
                table = sql.Identifier(n["table_e"]),
                c_1 = sql.Identifier(n["c_1"]),
                c_2 = sql.Identifier(n["c_2"]),
                c_4 = sql.Identifier(n["c_4"]),
                c_5 = sql.Identifier(n["c_5"]),
                c_id = sql.Identifier(n["c_id"])
                )
        try:
            with self.connection:
                with self.connection.cursor() as cur:
                    cur.execute(query, (c_1, c_2, c_4, c_5, c_id))
                    log.info("Удалось модифицировать информацию сотрудника")
                    return cur.rowcount
        except psycopg2.Error as error:
            log.error("не удалось модифицировать информацию сотрудника pgcode=%s", error.pgcode)
            raise RuntimeError("Не удалось модифицировать информацию сотрудника") from None

    def modify_employee_role_by_c1_c2(self, c_1, c_2, c_4):
        n = self._n

        query = sql.SQL(
            """
            UPDATE {table}
            SET {c_4} = %s
            WHERE {c_1} = %s AND {c_2}=%s;
            """
            ).format(
                table = sql.Identifier(n["table_e"]),
                c_1 = sql.Identifier(n["c_1"]),
                c_2 = sql.Identifier(n["c_2"]),
                c_4 = sql.Identifier(n["c_4"]),
            )
        try:
            with self.connection:
                with self.connection.cursor() as cursor:
                    cursor.execute(query, (c_4, c_1, c_2))
                    log.info("Удалось изменить роль сотрудника")
                    return cursor.rowcount
        except psycopg2.Error as error:
            log.error("не удалось изменить роль сотрудника pgcode=%s", error.pgcode)
            raise RuntimeError("Не удалось изменить роль сотрудника") from None

    def del_employee_by_id(self, c_id):
        n = self._n

        query = sql.SQL(
            """
            DELETE FROM {table}
            WHERE {c_id} = %s;
            """
        ).format(
            table = sql.Identifier(n["table_e"]),
            c_id = sql.Identifier(n["c_id"])
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