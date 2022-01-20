import json
import plotly
import plotly.express as px
import yfinance as yf
from flask import Flask, render_template, request, url_for, redirect

from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, login_user, current_user, LoginManager, logout_user

from flask_login import UserMixin

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mySecretKey*'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

login_manager = LoginManager() 		#
login_manager.login_view = 'Login'	#
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/", methods=['GET', 'POST'])
@login_required
def Index():
    if request.method == 'POST':
        # 3 Variablen an Input Formular zuweisen
        aktiensymbol = request.form["aktiensymbol"]
        anzahl = int(request.form["anzahl"])
        preis = float(request.form["preis"])

        try:
            usereingabe = yf.Ticker(
                aktiensymbol)  # Ticker ist für das Aktiensymbol welches der User durch Post request schickt
            marktpreis = usereingabe.info[
                "regularMarketPrice"]  # .info und regularmarketprice geben den aktuellen Marktpreis der Aktie an
            unternehmen = usereingabe.info["longName"]
            df = usereingabe.history(period="7d")
            df = df.reset_index()

            df['Open'] = df['Open'].astype('float64')
            fig = px.line(df, x='Date', y='Open',
                          labels={
                              "Date": "Datum",
                              "Open": "Marktpreis",
                          },
                          title=f'{unternehmen}\'s Preis in den letzten 7 Tagen')

            graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

            # dieses dictionary sind alle daten welche in der tabelle von index.html angezeigt werden
            result = {
                "aktiensymbol": aktiensymbol,
                "preis": f"{preis} $",
                "marktpreis": f"{marktpreis} $",
                "anzahl": anzahl,
                "gewinn": f"{round(anzahl * float(marktpreis - preis), 2)} $"
            }

            return render_template("index.html", result=result, graph_ready=True, graphJSON=graphJSON)
        except:
            # Fehlermeldung kommt falls jemand ein Aktiensymbol eingibt, welches nicht von yfinance unterstützt wird
            error = f"{aktiensymbol} ist ungültig! Bitte geben Sie ein anderes Aktiensymbol ein."
            return render_template('index.html', error=error)
    else:
        return render_template('index.html')

@app.route('/login/', methods = ['POST', 'GET'])
def Login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']


        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            error = 'Deine Login-Daten sind falsch, versuche es nochmals.'
            return render_template('login.html', error=error)
        else:
            login_user(user, remember=True)
            return redirect(url_for('Index'))

    return render_template('login.html')

@app.route('/register/', methods = ['POST', 'GET'])
def Register():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        password = request.form['password']

        try:
            new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('Login'))
        except Exception as e:
            error = e
    return render_template('register.html', error = error)

@app.route('/logout/')
@login_required
def Logout():
    logout_user()
    return redirect(url_for('Login'))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
