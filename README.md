# PRG-RA7

## Preparació del entorn
Per a deixar preparat el entorn per a treballar el projecte es necessari seguir els seguients pasos per a que puguem traballar amb seguretat.

Necesitarem:
- Accés a un repositori
    - On posarem una carpeta **venv**, la qual aillarà el entorn per a no patir incopatibilitats mitjançant un entorn virtual.
    - També ha de comptar amb un **.gitignore** on estara tot el que volem evitar muntar el repositori.

- Python instal·lat amb:
    - Versió 3.8 o superior

### Activar l'entorn virtual

Per crear l'entorn virtual entrarem per al terminal de Windows i executarem la següent comanda dins del repositori:
```
python -m venv venv 
```
Això crearà una carpeta **venv**, la qual també generarà el arxiu **.gitignore**, el qual menejaem fora de **venv** per a que quede així:
```
Repo\
    venv\
    .gitignore
```
Aqui afegirem tots els arxius que volem evitar que es munten.

Tot seguit, tambe haurem de activar l'entorn amb:
```
 .\venv\Scripts\activate
```

### Instal·lar llibreries

Per al projecte són necesaries les llibreries que es troben al arxiu requirements.txt, per instal·lar-les usarem:
```
pip install -r requirements.txt
```

### Iniciar el server

Per últim haurem de executar el arxiu app.py per iniciar el server amb:

```
python ./app.py
```
I amb això, entrant amb el navegador a 127.0.0.1:5000, ja haurem deixat preparat el entorn per començar a treballar el projecte.
