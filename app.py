from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

class Utilisateur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    abonnement = db.Column(db.String(50), nullable=False)

@app.route("/")
def accueil():
    return render_template("accueil.html")

@app.route("/utilisateurs")
def index():
    recherche = request.args.get("q", "")
    if recherche:
        utilisateurs = Utilisateur.query.filter(
            Utilisateur.nom.ilike(f"%{recherche}%") |
            Utilisateur.username.ilike(f"%{recherche}%")
        ).all()
    else:
        utilisateurs = Utilisateur.query.all()

    total = Utilisateur.query.count()
    free = Utilisateur.query.filter_by(abonnement="Free").count()
    normal = Utilisateur.query.filter_by(abonnement="Normal").count()
    vip = Utilisateur.query.filter_by(abonnement="VIP").count()

    return render_template("index.html",
        utilisateurs=utilisateurs,
        recherche=recherche,
        total=total, free=free,
        normal=normal, vip=vip)

@app.route("/ajouter", methods=["GET", "POST"])
def ajouter():
    print("=== MÉTHODE REÇUE :", request.method, "===")  # Debug
    if request.method == "POST":
        print("=== DONNÉES REÇUES :", request.form, "===")  # Debug
        nom = request.form.get("nom")
        username = request.form.get("username")
        abonnement = request.form.get("abonnement")
        print(f"Nom: {nom}, Username: {username}, Abonnement: {abonnement}")
        if nom and username and abonnement:
            nouvel_utilisateur = Utilisateur(nom=nom, username=username, abonnement=abonnement)
            db.session.add(nouvel_utilisateur)
            db.session.commit()
            print("=== UTILISATEUR AJOUTÉ AVEC SUCCÈS ===")
        return redirect(url_for("index"))
    return render_template("ajouter.html")

@app.route("/supprimer/<int:id>")
def supprimer(id):
    utilisateur = Utilisateur.query.get_or_404(id)
    db.session.delete(utilisateur)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)