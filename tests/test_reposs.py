import pytest
import os
import psycopg2

from dotenv import load_dotenv
from datetime import date

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

from repo_layer.schedule_shifts_db import SSRepo

@pytest.fixture
def repo(connection):
    return SSRepo(connection)

#def test_create_shift(repo):
    #result = repo.create_shift('2026-11-11', 1)
    #print("test create shift: ", result)
    #assert isinstance(result, object)

def test_get_shifts(repo):
    result = repo.get_shifts()
    print("get shifts: ")
    for row in result: print(row)
    assert isinstance(result, object)

def test_get_shift_by_date(repo):
    result = repo.get_shift_by_date('2026-11-12')
    print("get shifts by date: ", result)
    assert isinstance(result, object)