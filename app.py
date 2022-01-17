import json
import plotly
import plotly.express as px
import yfinance as yf
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
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


if __name__ == "__main__":
    app.run(debug=True, port=5000)
