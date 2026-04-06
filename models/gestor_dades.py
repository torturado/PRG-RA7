import csv
import os
from models.entities import Resultat

class GestorDades:
    def __init__(self):
        # Ruta de resultados
        self.ruta_resultats = 'dades/resultats.csv'

    # --- Gestion de Resultados ---
    def guardar_resultat(self, resultat_obj):
        """Recibe un objeto Resultat y lo añade al historico"""
        with open(self.ruta_resultats, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(resultat_obj.to_csv_row())

    def carregar_resultats(self):
        """Devuelve una lista de objetos Resultat"""
        resultats = []
        if not os.path.exists(self.ruta_resultats):
            return resultats

        with open(self.ruta_resultats, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if row:
                    resultats.append(Resultat(row[0], row[1], row[2], row[3]))
        return resultats
