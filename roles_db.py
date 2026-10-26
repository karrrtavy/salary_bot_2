from psycopg2 import sql

class RoleRepo:
    def __init__(self, connection):
        self.connection = connection

    def get_by_name(self, role_name):
        query = sql.SQL(
            """
            SELECT {id}, {role_name}, {hourly_rate}
            FROM {table} 
            WHERE {role_name} = %s;
            """
            ).format(
                id = sql.Identifier("id"),
                role_name = sql.Identifier("role_name"),
                hourly_rate = sql.Identifier("hourly_rate"),
                table = sql.Identifier("roles")
                )
        with self.connection.cursor() as cursor:
            cursor.execute(query, (role_name))
            return cursor.fetchone()