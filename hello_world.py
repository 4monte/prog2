from flask import Flask
from flask import render_template

app = Flask("Hello World")


@app.route("/hello")
def hello():
    return render_template('index.html', name="Sofia")

@app.route("/hello2/" , methods=['GET', 'POST'])
def hallo():
    if request.method == 'POST':
        return render_template("index.html")
    if request.method == 'POST':
        ziel_person = request.form['vorname']
        rueckgabe_string = "Hello " + ziel_person + "!"
        return rueckgabe_string


if __name__ == "__main__":
    app.run(debug=True, port=5000)