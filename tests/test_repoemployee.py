import psycopg2
import pytest
import os

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

from repo_layer.employees_db import EmployeesRepo
repo = EmployeesRepo(connection)

@pytest.fixture
def repo(connection):
    return EmployeesRepo(connection)

#def test_reg_emp(connection):
    #result = repo.registration_employee("Test", "Test", 1, 1)
    #assert isinstance(result, (type(None), object))

def test_get_emps(repo):
    result = repo.get_employees()
    print("test_get_emps: ")
    for row in result: print(row)
    assert isinstance(result, list)

def test_get_emp_by_id(repo):
    result = repo.get_employee_by_id(19)
    print("test_get_emp_by_id: ", result)
    assert isinstance(result, (type(None), object))

def test_get_emp_by_c12(repo):
    result = repo.get_employee_by_c1_c2("Test2", "Test")
    print("get_emp_by_c12: ", result)
    assert isinstance(result, object)

def test_modify_emp_by_id(repo):
    result = repo.modify_employee_by_id(19, "Newtest", "newtest", "1", "2")
    print("modify emp: ", result)
    assert isinstance(result, object)

def test_modify_emp_by_c12(repo):
    result = repo.modify_employee_role_by_c1_c2("Test2", "Test", 1)
    print("modify emp: ", result)
    assert isinstance(result, object)

