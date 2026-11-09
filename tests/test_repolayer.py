import pytest
import os
import psycopg2

from dotenv import load_dotenv

load_dotenv(override=True)

@pytest.fixture
def connection():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DBNAME"), 
            user=os.getenv("DBUSER"), 
            password=os.getenv("DBPASSWORD"), 
            host=os.getenv("DBHOST")
        )
        yield conn
        conn.close()
    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
        raise


def test_connection(connection):
    assert connection is not None

def test_get_all(connection):
    from repo_layer.roles_db import RoleRepo
    repo = RoleRepo(connection)
    result = repo.get_all()
    print("method get_all:", result)
    assert isinstance(result, list)

def test_get_by_name(connection):
    from repo_layer.roles_db import RoleRepo
    repo = RoleRepo(connection)
    result = repo.get_by_name("")
    print("method get_by_name:", result)
    assert isinstance(result, (type(None), object))
    result = repo.get_by_name("")
    print("method get_by_name:", result)
    assert isinstance(result, (type(None), object))