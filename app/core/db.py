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