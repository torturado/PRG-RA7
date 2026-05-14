from models.db import get_connection
from models.models import PartidaModel
from models.mongo import partides_collection


class GestorDades:
    def __init__(self):
        self.partides_collection = partides_collection

    def guardar_partida(self, partida_obj: PartidaModel):
        # primer comprobar mariadb, si la partida_obj es puntuacio > lla que ya esta dins, guardar mariadb else continua mongo
        partida = (
            partida_obj
            if isinstance(partida_obj, PartidaModel)
            else PartidaModel.model_validate(partida_obj)
        )

        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT MAX(puntuacio) AS max_puntuacio FROM partides WHERE joc_nom = %s AND username = %s",
                    (partida.joc_nom, partida.username),
                )
                row = cursor.fetchone()
                max_anterior = row["max_puntuacio"] if row else None
                if max_anterior is None or partida.puntuacio > max_anterior:
                    cursor.execute(
                        "UPDATE partides SET puntuacio = %s, data_hora = %s, errors = %s WHERE joc_nom = %s and username = %s",
                        (
                            partida.puntuacio,
                            partida.data_hora,
                            partida.errors,
                            partida.joc_nom,
                            partida.username,
                        ),
                    )
                    if cursor.rowcount == 0:
                        cursor.execute(
                            "INSERT INTO partides (username, joc_nom, puntuacio, data_hora, errors) VALUES (%s, %s, %s, %s, %s)",
                            (
                                partida.username,
                                partida.joc_nom,
                                partida.puntuacio,
                                partida.data_hora,
                                partida.errors,
                            ),
                        )
                    conn.commit()

                doc = partida.model_dump(exclude={"id"})
                self.partides_collection.insert_one(doc)

    def carregar_resultats(self, joc_nom: str):
        return self.partides_collection.find({"joc_nom": joc_nom})

    def carregar_resultats_mariadb(self, joc_nom: str):
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT username, puntuacio, data_hora, COALESCE(errors, 0) AS errors
                    FROM partides
                    WHERE joc_nom = %s
                    ORDER BY puntuacio DESC, data_hora DESC
                    """,
                    (joc_nom,),
                )
                return cursor.fetchall()
