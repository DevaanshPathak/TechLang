# techlang/database.py

import sqlite3
import os
from typing import List, Dict, Any, Optional
from .core import InterpreterState


class DatabaseHandler:
    """Handles SQLite3 database operations in TechLang."""
    
    _instance = None
    
    def __new__(cls):
        """Singleton pattern to ensure only one instance exists."""
        if cls._instance is None:
            cls._instance = super(DatabaseHandler, cls).__new__(cls)
            cls._instance.connections: Dict[str, sqlite3.Connection] = {}
            cls._instance.default_db = "techlang.db"
        return cls._instance
    
    def get_connection(self, db_name: Optional[str] = None) -> sqlite3.Connection:
        """
        Get or create a database connection.
        
        Args:
            db_name: Database name (defaults to techlang.db)
            
        Returns:
            SQLite connection object
        """
        if db_name is None:
            db_name = self.default_db
        
        if db_name not in self.connections:
            # Create connection
            conn = sqlite3.connect(db_name)
            conn.row_factory = sqlite3.Row  # Enable dict-like access
            self.connections[db_name] = conn
        
        return self.connections[db_name]
    
    def close_connection(self, db_name: Optional[str] = None) -> None:
        """
        Close a database connection.
        
        Args:
            db_name: Database name (defaults to techlang.db)
        """
        if db_name is None:
            db_name = self.default_db
        
        if db_name in self.connections:
            self.connections[db_name].close()
            del self.connections[db_name]
    
    def close_all_connections(self) -> None:
        """Close all database connections."""
        for db_name in list(self.connections.keys()):
            self.close_connection(db_name)
    
    @staticmethod
    def handle_db_create(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Handle the 'db_create' command to create a table.
        
        Args:
            state: The interpreter state
            tokens: List of tokens
            index: Current token index
            
        Returns:
            Number of tokens consumed
        """
        if index + 2 >= len(tokens):
            state.add_error("db_create requires table name and columns")
            return 0
        
        table_name = tokens[index + 1]
        columns_str = tokens[index + 2]
        
        try:
            # Remove quotes from columns string
            if columns_str.startswith('"') and columns_str.endswith('"'):
                columns_str = columns_str[1:-1]
            
            # Parse columns (format: "col1 type1, col2 type2, ...")
            columns = []
            for col_def in columns_str.split(','):
                col_def = col_def.strip()
                if ' ' in col_def:
                    # Handle cases like "id INTEGER PRIMARY KEY"
                    parts = col_def.split()
                    col_name = parts[0]
                    col_type = ' '.join(parts[1:])  # Join all remaining parts as the type
                    columns.append(f"{col_name.strip()} {col_type.strip()}")
                else:
                    state.add_error(f"Invalid column definition: {col_def}")
                    return 2
            
            # Create table
            db_handler = DatabaseHandler()
            conn = db_handler.get_connection()
            cursor = conn.cursor()
            
            columns_sql = ', '.join(columns)
            sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_sql})"
            cursor.execute(sql)
            conn.commit()
            
            state.add_output(f"Table '{table_name}' created successfully")
            return 2  # Consume table name and columns
            
        except Exception as e:
            state.add_error(f"Failed to create table: {str(e)}")
            return 2
    
    @staticmethod
    def handle_db_insert(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Handle the 'db_insert' command to insert data.
        
        Args:
            state: The interpreter state
            tokens: List of tokens
            index: Current token index
            
        Returns:
            Number of tokens consumed
        """
        if index + 2 >= len(tokens):
            state.add_error("db_insert requires table name and values")
            return 0
        
        table_name = tokens[index + 1]
        values_str = tokens[index + 2]
        
        try:
            # Remove quotes from values string
            if values_str.startswith('"') and values_str.endswith('"'):
                values_str = values_str[1:-1]
            
            # Parse values (format: "val1, val2, val3, ...")
            values = [v.strip() for v in values_str.split(',')]
            
            # Create placeholders
            placeholders = ', '.join(['?' for _ in values])
            
            db_handler = DatabaseHandler()
            conn = db_handler.get_connection()
            cursor = conn.cursor()
            
            sql = f"INSERT INTO {table_name} VALUES ({placeholders})"
            cursor.execute(sql, values)
            conn.commit()
            
            state.add_output(f"Inserted {cursor.rowcount} row(s) into '{table_name}'")
            return 2  # Consume table name and values
            
        except Exception as e:
            state.add_error(f"Failed to insert data: {str(e)}")
            return 2
    
    @staticmethod
    def handle_db_select(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Handle the 'db_select' command to query data.
        
        Args:
            state: The interpreter state
            tokens: List of tokens
            index: Current token index
            
        Returns:
            Number of tokens consumed
        """
        if index + 1 >= len(tokens):
            state.add_error("db_select requires a SQL query")
            return 0
        
        query = tokens[index + 1]
        
        try:
            # Remove quotes from query
            if query.startswith('"') and query.endswith('"'):
                query = query[1:-1]
            
            db_handler = DatabaseHandler()
            conn = db_handler.get_connection()
            cursor = conn.cursor()
            
            cursor.execute(query)
            rows = cursor.fetchall()
            
            if rows:
                # Get column names
                columns = [description[0] for description in cursor.description]
                state.add_output(f"Columns: {', '.join(columns)}")
                
                # Output rows
                for i, row in enumerate(rows):
                    row_data = [str(row[col]) for col in columns]
                    state.add_output(f"Row {i+1}: {', '.join(row_data)}")
            else:
                state.add_output("No rows found")
            
            return 1  # Consume query
            
        except Exception as e:
            state.add_error(f"Failed to execute query: {str(e)}")
            return 1
    
    @staticmethod
    def handle_db_update(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Handle the 'db_update' command to update data.
        
        Args:
            state: The interpreter state
            tokens: List of tokens
            index: Current token index
            
        Returns:
            Number of tokens consumed
        """
        if index + 1 >= len(tokens):
            state.add_error("db_update requires a SQL query")
            return 0
        
        query = tokens[index + 1]
        
        try:
            # Remove quotes from query
            if query.startswith('"') and query.endswith('"'):
                query = query[1:-1]
            
            db_handler = DatabaseHandler()
            conn = db_handler.get_connection()
            cursor = conn.cursor()
            
            cursor.execute(query)
            conn.commit()
            
            state.add_output(f"Updated {cursor.rowcount} row(s)")
            return 1  # Consume query
            
        except Exception as e:
            state.add_error(f"Failed to execute update: {str(e)}")
            return 1
    
    @staticmethod
    def handle_db_delete(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Handle the 'db_delete' command to delete data.
        
        Args:
            state: The interpreter state
            tokens: List of tokens
            index: Current token index
            
        Returns:
            Number of tokens consumed
        """
        if index + 1 >= len(tokens):
            state.add_error("db_delete requires a SQL query")
            return 0
        
        query = tokens[index + 1]
        
        try:
            # Remove quotes from query
            if query.startswith('"') and query.endswith('"'):
                query = query[1:-1]
            
            db_handler = DatabaseHandler()
            conn = db_handler.get_connection()
            cursor = conn.cursor()
            
            cursor.execute(query)
            conn.commit()
            
            state.add_output(f"Deleted {cursor.rowcount} row(s)")
            return 1  # Consume query
            
        except Exception as e:
            state.add_error(f"Failed to execute delete: {str(e)}")
            return 1
    
    @staticmethod
    def handle_db_execute(state: InterpreterState, tokens: List[str], index: int) -> int:
        """
        Handle the 'db_execute' command to execute any SQL.
        
        Args:
            state: The interpreter state
            tokens: List of tokens
            index: Current token index
            
        Returns:
            Number of tokens consumed
        """
        if index + 1 >= len(tokens):
            state.add_error("db_execute requires a SQL statement")
            return 0
        
        sql = tokens[index + 1]
        
        try:
            # Remove quotes from SQL
            if sql.startswith('"') and sql.endswith('"'):
                sql = sql[1:-1]
            
            db_handler = DatabaseHandler()
            conn = db_handler.get_connection()
            cursor = conn.cursor()
            
            cursor.execute(sql)
            
            # Check if it's a SELECT query
            if sql.strip().upper().startswith('SELECT'):
                rows = cursor.fetchall()
                if rows:
                    columns = [description[0] for description in cursor.description]
                    state.add_output(f"Columns: {', '.join(columns)}")
                    for i, row in enumerate(rows):
                        row_data = [str(row[col]) for col in columns]
                        state.add_output(f"Row {i+1}: {', '.join(row_data)}")
                else:
                    state.add_output("No rows found")
            else:
                conn.commit()
                state.add_output(f"Executed successfully. Rows affected: {cursor.rowcount}")
            
            return 1  # Consume SQL statement
            
        except Exception as e:
            state.add_error(f"Failed to execute SQL: {str(e)}")
            return 1
    
    @staticmethod
    def handle_db_close(state: InterpreterState) -> None:
        """
        Handle the 'db_close' command to close database connections.
        
        Args:
            state: The interpreter state
        """
        try:
            db_handler = DatabaseHandler()
            db_handler.close_all_connections()
            state.add_output("All database connections closed")
        except Exception as e:
            state.add_error(f"Failed to close connections: {str(e)}")
