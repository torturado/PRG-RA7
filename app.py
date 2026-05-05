from flask import (
    Flask,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from models.db import init_db
from models.gestor_dades import GestorDades
from models.jocs import JocDisponible
from models.usuaris import Usuari

app = Flask(__name__)
gestor = GestorDades()
init_db()
app.secret_key = "clau_secreta_ic_games_1r_daw"


@app.context_processor
def inject_usuari():
    """Fa que el usuari estigui disponible a totes les plantilles."""
    return {"usuari": session.get("usuari_actiu")}


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        nom = request.form.get("username")
        clau = request.form.get("password")

        usuari_actual = Usuari(nom, clau)

        if usuari_actual.validar_acces():
            session["usuari_actiu"] = nom
            return redirect(url_for("home"))
        else:
            flash("Accés denegat: Credencials incorrectes.", "error")

    return render_template("login.html")


@app.route("/registre", methods=["GET", "POST"])
def registre():
    if request.method == "POST":
        nom = request.form.get("username")
        clau = request.form.get("password")

        nou_usuari = Usuari(nom, clau)

        if nou_usuari.guardar_en_bd():
            flash("Registrat amb èxit, ja pots iniciar el protocol.", "success")
            return redirect(url_for("login"))
        else:
            flash("Error: L'identificador d'usuari ja està en ús.", "error")

    return render_template("registre.html")


@app.route("/home")
def home():
    if "usuari_actiu" in session:
        nom_usuari = session["usuari_actiu"]
        jocs_disponibles = JocDisponible.llistar_actius()
        return render_template("home.html", usuari=nom_usuari, jocs=jocs_disponibles)
    else:
        flash("Protocol de seguretat: Has d'iniciar sessió primer.", "error")
        return redirect(url_for("login"))


@app.route("/logout", methods=["POST"])
def logout():
    session.pop("usuari_actiu", None)
    flash("Sessió tancada correctament.", "success")
    return redirect(url_for("login"))


@app.route("/joc1")
def joc1():
    if "usuari_actiu" in session:
        return render_template("joc1.html", usuari=session["usuari_actiu"])
    else:
        flash("Protocol de seguretat: Identifica't per jugar.", "error")
        return redirect(url_for("login"))


@app.route("/joc2")
def joc2():
    if "usuari_actiu" in session:
        return render_template("joc2.html", usuari=session["usuari_actiu"])
    else:
        flash("Protocol de seguretat: Identifica't per jugar.", "error")
        return redirect(url_for("login"))


@app.route("/joc3")
def joc3():
    if "usuari_actiu" in session:
        return render_template("joc3.html", usuari=session["usuari_actiu"])
    else:
        flash("Protocol de seguretat: Identifica't per jugar.", "error")
        return redirect(url_for("login"))


@app.route("/finalitzar_joc", methods=["POST"])
def finalitzar_joc():
    dades = request.get_json()
    username = session.get("usuari_actiu")
    puntuacio = int(dades.get("puntuacio", 0))
    joc_nom = dades.get("joc", "Joc")
    data = dades.get("data")
    errors = dades.get("errors", 0)
    resultat = {
        "username": username,
        "joc_nom": joc_nom,
        "puntuacio": puntuacio,
        "data_hora": data,
        "errors": errors,
    }
    print(resultat)
    gestor.guardar_partida(resultat)
    print(f"Partida finalitzada per {username}: {puntuacio} punts. Guardat a MongoDB")
    return jsonify({"status": "success"})


@app.route("/rankings")
def rankings():
    joc_seleccionat = request.args.get("joc", "Selecció en ordre")
    dades_ranking = gestor.carregar_resultats_mariadb(joc_seleccionat)

    return render_template(
        "rankings.html",
        usuari=session.get("usuari_actiu"),
        dades=dades_ranking,
        joc_seleccionat=joc_seleccionat,
    )


@app.route("/api/stats_dashboard")
def api_stats_dashboard():
    if "usuari_actiu" not in session:
        return jsonify({"error": "Sessio requerida"}), 401
    nom_usuari = session["usuari_actiu"]
    from models.mongo import partides_collection
    pipeline_jugades = [
        {"$match": {"username": nom_usuari}},
        {"$group": {
            "_id": "$joc_nom", 
            "total_jugades": {"$sum": 1}
        }}
    ]
    dades_jugades_crues = list(partides_collection.aggregate(pipeline_jugades))
    
    noms_jocs_jugades = [doc["_id"] for doc in dades_jugades_crues]
    total_jugades = [doc["total_jugades"] for doc in dades_jugades_crues]
    pipeline_historic = [
        {"$match": {"username": nom_usuari}},
        {"$sort": {"data_hora": 1}}
    ]
    dades_historic = list(partides_collection.aggregate(pipeline_historic))
    dates_joc = []
    for doc in dades_historic:
        dh = doc.get("data_hora")
        if dh:
            if isinstance(dh, str):
                dates_joc.append(dh[:16].replace("T", " "))
            else:
                try:
                    dates_joc.append(dh.strftime("%d/%m %H:%M"))
                except:
                    dates_joc.append(str(dh))
    historic_puntuacions = [doc.get("puntuacio", 0) for doc in dades_historic]
    noms_jocs_historic = [doc.get("joc_nom", "") for doc in dades_historic]
    return jsonify({
        "jugades": {
            "noms_jocs": noms_jocs_jugades,
            "totals": total_jugades
        },
        "historic": {
            "dates": dates_joc,
            "puntuacions": historic_puntuacions,
            "jocs": noms_jocs_historic
        }
    })


@app.route("/dashboard")
def veure_dashboard():
    if "usuari_actiu" not in session:
        flash("Cal iniciar sessió", "error")
        return redirect(url_for("login"))
    return render_template("dashboard.html", usuari=session["usuari_actiu"])



if __name__ == "__main__":
    app.run(debug=True)
