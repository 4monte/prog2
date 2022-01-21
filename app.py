import json
import plotly
import plotly.express as px
import yfinance as yf
from flask import Flask, render_template, request, url_for, redirect
# folgendes ist um das Passwort zu hashen und überprüfen
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, login_user, LoginManager, logout_user

from flask_login import UserMixin

app = Flask(__name__)

# secret key ist ein Passwort um die Authentifizierung zulassen zu können
# wenn kein secret key definiert ist, gibt Flask eine Fehlermeldung
# und das flask_login modul wäre nutzlos
app.config["SECRET_KEY"] = "mySecretKey*"

# folgendes verbindet die Datenbank mit dem Programm
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"

# folgend wird db erstellt, was über SQLAlchemy mit der Flask App verbunden ist
db = SQLAlchemy(app)


# Datenbank Tabelle namens User mit 4 Spalten wird erstellt
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


login_manager = LoginManager()  # login_manager wird aus dem LoginManager Modul erstellt
login_manager.login_view = "Login"  # Wenn der User nicht eingeloggt ist kommt diese Seite
login_manager.init_app(app) # das erstellte login_manager wird mit App verbunden


# diese Funktion ist für login_required erforderlich, da sie den autentifizierten Benutzer zurückgibt
# mehr dazu: https://flask-login.readthedocs.io/en/latest/
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/", methods=["GET", "POST"])
@login_required # der Benutzer wird zur Login Seite weitergeleitet
def Index():
    if request.method == "POST":
        # 3 Variablen an Input Formular zuweisen
        aktiensymbol = request.form["aktiensymbol"]
        anzahl = int(request.form["anzahl"])
        preis = float(request.form["preis"])

        try:
            usereingabe = yf.Ticker(
                aktiensymbol
            )  # Ticker ist für das Aktiensymbol welches der User durch Post request schickt
            marktpreis = usereingabe.info[
                "regularMarketPrice"
            ]  # .info und regularmarketprice geben den aktuellen Marktpreis der Aktie an
            unternehmen = usereingabe.info[
                "longName"
            ]  # longName gibt den vollen Namen des Unternehmens an, dies wird über dem Graph angezeigt
            df = usereingabe.history(period="7d") # dies gibt pandas dataframe zurück
                                                  # mehr dazu: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html
            df = df.reset_index() # formatiert die Tabelle und ermöglicht anschliessend die ['xxx'] Abfrage
                                  # somit kann man die Daten mit Plotly verwenden
                                  # mehr dazu: https://www.geeksforgeeks.org/python-pandas-dataframe-reset_index/

            # für den Key "Open" wandeln wir alles in float um, und 64 steht für bits
            # float wird benötigt, damit es in plotly geplotted werden kann
            # mehr dazu: https://plotly.com/python/line-charts/
            df["Open"] = df["Open"].astype("float64")

            # folgend wurden die labels erstellt, damit auf dem Graph der Ausdruck auf Deutsch ist
            # fig.update wird verwendet um den weissen Hintergrund zu entfernen
            fig = px.line(
                df,
                x="Date",
                y="Open",
                labels={
                    "Date": "Datum",
                    "Open": "Marktpreis",
                },
                title=f"{unternehmen}'s Preis in den letzten 7 Tagen",
            )
            fig.update_layout(plot_bgcolor="rgba(255,255,255,0)")


            graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

            # dieses dictionary sind alle daten welche in der tabelle von index.html angezeigt werden
            result = {
                "aktiensymbol": aktiensymbol,
                "preis": f"{preis} $",
                "marktpreis": f"{marktpreis} $",
                "anzahl": anzahl,
                "gewinn": f"{round(anzahl * float(marktpreis - preis), 2)} $",
            }

            return render_template(
                "index.html", result=result, graph_ready=True, graphJSON=graphJSON
            )
        except:
            # Fehlermeldung kommt falls jemand ein Aktiensymbol eingibt, welches nicht von yfinance unterstützt wird
            error = f"{aktiensymbol.upper()} ist ungültig! Bitte gebe ein anderes Aktiensymbol ein."
            return render_template("index.html", error=error)
    else:
        return render_template("index.html")


@app.route("/login/", methods=["POST", "GET"])
def Login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        # der eingeloggte Benutzer wird abgefragt
        # wenn er nicht existiert, kommt er nicht durch die nächste if funktion
        user = User.query.filter_by(email=email).first()

        # passwort und user werden nochmals überprüft
        # check_password_hash -> vergleich Eingabe mit dem Passwort in der Datenbank
        if not user or not check_password_hash(user.password, password):
            error = "Deine Login-Daten sind falsch, versuche es nochmals."
            return render_template("login.html", error=error)
        else:
            login_user(user, remember=True) # Benutzer wird eingeloggt
                                            # durch remember kann er die Seite neu laden und bleibt eingeloggt
            # redirect -> leitet Benutzer auf URL weiter
            # url_for -> gibt die URL mit dem Namen des strings zurück
            return redirect(url_for("Index"))

    return render_template("login.html")


@app.route("/register/", methods=["POST", "GET"])
def Register():
    error = None
    if request.method == "POST":
        email = request.form["email"]
        name = request.form["name"]
        password = request.form["password"]

        try:
            # generate_password_hash -> hasht das eingegebene passwort
            # wenn die Datenbank gehackt werden würde, bekäme man nur das gehashte Passwort
            # sha256 ist eine Hashfunktion, welche praktisch unmöglich ist um zu entschlüsseln
            new_user = User(
                email=email,
                name=name,
                password=generate_password_hash(password, method="sha256"),
            )
            # new_user wird der Datenbank eingefügt
            db.session.add(new_user)
            # die Änderung wird committed
            db.session.commit()
            # sobald der Benutzer sich erfolgreich registriert hat wird er der Loginseite weitergeleitet
            return redirect(url_for("Login"))
        except:
            # Fehlermeldung falls E-Mail bereits verwendet wird.
            error = "Deine E-Mail wird bereits verwendet."
    return render_template("register.html", error=error)


@app.route("/logout/")
@login_required
def Logout():
    # diese Funktion loggt den Benutzer aus
    logout_user()
    # danach wird er zur Loginseite weitergeleitet
    return redirect(url_for("Login"))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
