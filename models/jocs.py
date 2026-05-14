from models.db import get_connection


class JocDisponible:
    def __init__(self, id, nom, actiu):
        self.id = id
        self.nom = nom
        self.actiu = bool(actiu)

    @classmethod
    def llistar_actius(cls):
        query = "SELECT id, nom, actiu FROM jocs WHERE actiu = 1 ORDER BY nom ASC"
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                files = cursor.fetchall()

        return [cls(fila["id"], fila["nom"], fila["actiu"]) for fila in files]
