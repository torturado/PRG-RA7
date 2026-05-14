import pymysql
from werkzeug.security import check_password_hash, generate_password_hash
from models.db import get_connection

class Usuari:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def guardar_en_bd(self):
        if self.existeix():
            return False

        password_hash = generate_password_hash(self.password)
        query = "INSERT INTO usuaris (usuari, contrasenya) VALUES (%s, %s)"
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (self.username, password_hash))
        except pymysql.MySQLError:
            return False
        return True

    def existeix(self):
        query = "SELECT 1 FROM usuaris WHERE usuari = %s LIMIT 1"
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (self.username,))
                return cursor.fetchone() is not None

    def validar_acces(self):
        query = "SELECT contrasenya FROM usuaris WHERE usuari = %s LIMIT 1"
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (self.username,))
                fila = cursor.fetchone()
                if not fila:
                    return False
                return check_password_hash(fila["contrasenya"], self.password)
