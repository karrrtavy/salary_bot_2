import sqlite3

class Database:
    def __init__(self):
        try:
            self.connection = sqlite3.connect('salary.db')
            self.connection.execute("PRAGMA foreign_keys = ON")
        except sqlite3.Error as error:
            raise RuntimeError("Не удалось подключиться к БД") from error
        
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                            CREATE TABLE IF NOT EXISTS "objects" (
                                id INTEGER PRIMARY KEY,
                                address TEXT
                            );
                            ''')
            cursor.execute('''
                            CREATE TABLE IF NOT EXISTS "employees" (
                                id INTEGER PRIMARY KEY,
                                surname TEXT NOT NULL,
                                name TEXT NOT NULL,
                                patronymic TEXT NOT NULL,
                                object_id INTEGER NOT NULL REFERENCES objects(id),
                                role_id INTEGER NOT NULL REFERENCES roles(id)
                            );
                            ''')
            cursor.execute('''
                            CREATE TABLE IF NOT EXISTS "roles" (
                                id INTEGER PRIMARY KEY,
                                role_name	TEXT NOT NULL UNIQUE,
                                hourly_rate REAL NOT NULL
                            );
                            ''')
            cursor.execute('''
                            CREATE TABLE IF NOT EXISTS "shifts" (
                                id INTEGER PRIMARY KEY,
                                shift_date TEXT NOT NULL,
                                start_shift TEXT NOT NULL,
                                end_shift TEXT NOT NULL,
                                hours REAL NOT NULL,
                                employee_id INTEGER NOT NULL REFERENCES employees(id),
                                revenue REAL
                            );
                            ''')
            cursor.execute('''
                            CREATE TABLE IF NOT EXISTS income (
                                id INTEGER PRIMARY KEY,
                                summ REAL,
                                shift_id INTEGER REFERENCES shifts(id)
                            );
                            ''')
            self.connection.commit()
        except sqlite3.Error as error:
            self.connection.rollback()
            self.connection.close()
            raise RuntimeError("Не удалось создать таблицы БД") from error

    def close(self):
        self.connection.close()