import os
import pymysql
from core.config import settings

# Database connection function
def get_db_connection() -> pymysql.connections.Connection:
    return pymysql.connect(
        host=settings.DB_HOST,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        database=settings.DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

def drop_all():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if any tables exist
    with open('/app/db/migrations/drop_all.sql', 'r') as file:
        ddl_commands = file.read()
        for command in ddl_commands.split(';'):
            command = command.strip()
            if command:  # Execute only non-empty commands
                cursor.execute(command)

    conn.commit()
    cursor.close()
    conn.close()
def apply_ddl_if_needed():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if any tables exist
    cursor.execute("SHOW TABLES;")
    tables = cursor.fetchall()

    if not tables:  # No tables found, apply DDL
        print("No tables found. Applying DDL...")
        with open('/app/db/migrations/ddl.sql', 'r') as file:
            ddl_commands = file.read()
            for command in ddl_commands.split(';'):
                command = command.strip()
                if command:  # Execute only non-empty commands
                    cursor.execute(command)
    else:
        print("Tables already exist. Skipping DDL application.")

    conn.commit()
    cursor.close()
    conn.close()

def init_test_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if any tables exist
    with open('/app/db/migrations/init_test.sql', 'r') as file:
        ddl_commands = file.read()
        for command in ddl_commands.split(';'):
            command = command.strip()
            if command:  # Execute only non-empty commands
                cursor.execute(command)

    conn.commit()
    cursor.close()
    conn.close()