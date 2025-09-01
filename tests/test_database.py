# tests/test_database.py

import os
import tempfile
import shutil
from techlang.interpreter import run


def cleanup_database():
    """Clean up any existing database file."""
    if os.path.exists("techlang.db"):
        # Close any existing connections first
        try:
            from techlang.database import DatabaseHandler
            db_handler = DatabaseHandler()
            db_handler.close_all_connections()
        except:
            pass
        try:
            os.remove("techlang.db")
        except:
            pass


def test_db_create_table():
    """Test creating a table."""
    code = """
    db_create users "id INTEGER PRIMARY KEY, name TEXT, age INTEGER"
    """
    output = run(code)
    assert "Table 'users' created successfully" in output


def test_db_insert_and_select():
    """Test inserting and selecting data."""
    cleanup_database()
    
    code = """
    db_create users "id INTEGER PRIMARY KEY, name TEXT, age INTEGER"
    db_insert users "1, Alice, 25"
    db_insert users "2, Bob, 30"
    db_select "SELECT * FROM users"
    """
    output = run(code)
    assert "Table 'users' created successfully" in output
    assert "Inserted 1 row(s) into 'users'" in output
    assert "Columns: id, name, age" in output
    assert "Row 1: 1, Alice, 25" in output
    assert "Row 2: 2, Bob, 30" in output


def test_db_update():
    """Test updating data."""
    cleanup_database()
    
    code = """
    db_create users "id INTEGER PRIMARY KEY, name TEXT, age INTEGER"
    db_insert users "1, Alice, 25"
    db_update "UPDATE users SET age = 26 WHERE name = 'Alice'"
    db_select "SELECT * FROM users WHERE name = 'Alice'"
    """
    output = run(code)
    assert "Updated 1 row(s)" in output
    assert "Row 1: 1, Alice, 26" in output


def test_db_delete():
    """Test deleting data."""
    cleanup_database()
    
    code = """
    db_create users "id INTEGER PRIMARY KEY, name TEXT, age INTEGER"
    db_insert users "1, Alice, 25"
    db_insert users "2, Bob, 30"
    db_delete "DELETE FROM users WHERE name = 'Alice'"
    db_select "SELECT * FROM users"
    """
    output = run(code)
    assert "Deleted 1 row(s)" in output
    assert "Row 1: 2, Bob, 30" in output
    assert "Alice" not in output


def test_db_execute():
    """Test executing custom SQL."""
    cleanup_database()
    
    code = """
    db_execute "CREATE TABLE test (id INTEGER, name TEXT)"
    db_execute "INSERT INTO test VALUES (1, 'test')"
    db_execute "SELECT * FROM test"
    """
    output = run(code)
    assert "Executed successfully" in output
    assert "Columns: id, name" in output
    assert "Row 1: 1, test" in output


def test_db_close():
    """Test closing database connections."""
    cleanup_database()
    
    code = """
    db_create users "id INTEGER PRIMARY KEY, name TEXT"
    db_close
    """
    output = run(code)
    assert "All database connections closed" in output


def test_database_error_handling():
    """Test error handling for invalid SQL."""
    code = """
    db_select "SELECT * FROM nonexistent_table"
    """
    output = run(code)
    assert "Failed to execute query" in output


if __name__ == "__main__":
    # Clean up any existing database files
    if os.path.exists("techlang.db"):
        os.remove("techlang.db")
    
    # Run tests
    test_db_create_table()
    test_db_insert_and_select()
    test_db_update()
    test_db_delete()
    test_db_execute()
    test_db_close()
    test_database_error_handling()
    
    print("All database tests passed!")
    
    # Clean up
    if os.path.exists("techlang.db"):
        os.remove("techlang.db")
