from psycopg2 import sql

class EmployeesRepo:
    def __init__(self, connection):
        self.connection = connection

    def get_employees(self):
        query = sql.SQL(
            """
            SELECT * FROM {table};
            """
        ).format(
            table = sql.Identifier("employees")
        )
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    def get_employee_4m_id(self, id):
        query = sql.SQL(
            """
            SELECT * FROM {table}
            WHERE {id} = %s;
            """
            ).format(
                table = sql.Identifier("employees"),
                id = sql.Identifier("id")
            )
        with self.connection.cursor() as cursor:
            cursor.execute(query, (id))
            return cursor.fetchone()

    def get_employee_4m_surname(self, surname):
        query = sql.SQL(
            """
            SELECT * FROM {table}
            WHERE {surname} = %s;
            """
            ).format(
                table = sql.Identifier("employees"),
                surname = sql.Identifier("surname")
            )
        with self.connection.cursor() as cursor:
            cursor.execute(query, (surname))
            return cursor.fetchone()
        
    def get_employee_4m_name(self, name):
        query = sql.SQL(
            """
            SELECT * FROM {table}
            WHERE {name} = %s;
            """
            ).format(
                table = sql.Identifier("employees"),
                name = sql.Identifier("name")
            )
        with self.connection.cursor() as cursor:
            cursor.execute(query, (name))
            return cursor.fetchone()

    def add_employee (self, surname, name, patronymic, object_id, role_id):
            query = sql.SQL(
                """
                INSERT INTO {table}({surname}, {name}, {patronymic}, {object_id}, {role_id}) 
                VALUES (%s, %s, %s, %s, %s)
                RETURNING {id};
                """
                ).format(
                    table = sql.Identifier("employees"),
                    surname = sql.Identifier("surname"),
                    name = sql.Identifier("name"),
                    patronymic = sql.Identifier("patronymic"),
                    object_id = sql.Identifier("object_id"),
                    role_id = sql.Identifier("role_id"),
                    id = sql.Identifier("id")
                    )
            with self.connection:
                with self.connection.cursor() as cursor:
                    cursor.execute(query, (surname, name, patronymic, object_id, role_id))
                    return cursor.fetchone()[0]

    def del_employee(self, employee_id):
        query = sql.SQL(
            """
            DELETE FROM {table}
            WHERE {id} = %s;
            """
        ).format(
            table = sql.Identifier("employees"),
            id = sql.Identifier("id")
            )
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute(query, (employee_id))
                return cursor.rowcount 

    def modify_employee(self, surname, name, patronymic, object_id, role_id, id):
        query = sql.SQL("""
                        UPDATE {table}
                        SET {surname} = %s,
                        {name} = %s,
                        {patronymic} = %s,
                        {object_id} = %s,
                        {role_id} = %s
                        WHERE {id} = %s;
                        """
                        ).format(
                            table = sql.Identifier("employees"),
                            surname = sql.Identifier("surname"),
                            name = sql.Identifier("name"),
                            patronymic = sql.Identifier("patronymic"),
                            object_id = sql.Identifier("object_id"),
                            role_id = sql.Identifier("role_id"),
                            id = sql.Identifier("id")
                        )
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute(query, (surname, name, patronymic, object_id, role_id, id))
                return cursor.rowcount


    def modify_employee_role(self, role_id, id):
        query = sql.SQL(
            """
            UPDATE {table}
            SET {role_id} = %s
            WHERE {id} = %s;
            """
            ).format(
                table = sql.Identifier("employees"),
                role_id = sql.Identifier("role_id"),
                id = sql.Identifier("id")
            )
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute(query, (role_id, id))
                return cursor.rowcount