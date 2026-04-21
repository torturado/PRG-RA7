import os
import pymysql
from dotenv import load_dotenv


load_dotenv()


def get_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", "3308")),
        user=os.getenv("DB_USER", "icgames_user"),
        password=os.getenv("DB_PASSWORD", "icgames1234"),
        database=os.getenv("DB_NAME", "icgames"),
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True,
    )


def init_db():
    query = """
    CREATE TABLE IF NOT EXISTS usuaris (
        id INT AUTO_INCREMENT PRIMARY KEY,
        usuari VARCHAR(80) NOT NULL UNIQUE,
        contrasenya VARCHAR(255) NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
