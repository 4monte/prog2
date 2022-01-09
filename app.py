from flask import Flask, render_template
import yfinance as yf



app = Flask(__name__)

@app.route("/" , methods=['GET', 'POST'])
def Index():

    if request.method == 'POST':
        # 3 Variablen an Input Formular zuweisen
        aktiensymbol = request.form["aktiensymbol"]
        anzahl = request.form["anzahl"]
        preis = request.form["preis"]

        try:
            usereingabe = yf.Ticker(aktiensymbol)
            marktpreis = usereingabe.info["regularMarketPrice"]

            ausgabe = {
                "aktiensymbol" : aktiensymbol,
                "preis" : preis
                "marktpreis" : marktpreis,
                "anzahl" : anzahl,
                "gewinn" : anzahl * float(marktpreis-preis)
            }
            return render_template("index.html", ausgabe=ausgabe)
        except:
            error= f"{aktiensymbol} ist ungültig!"
            return render_template('index.html', error=error)
    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True, port=5000)