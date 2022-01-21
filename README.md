# Aktien Portfolio Web App

Eine App, welche es ermöglicht Aktiengewinne/ -verluste auszurechnen und Aktienkurse anzusehen.

## Projektbeschreibung und Anleitung (1-3)

### 1. Login und registrieren

Die Web App startet mit der Login Seite. Falls man noch kein Login hat, kann man auf der Navbar auf Registrieren klicken und kommt somit auf die Registrieren Seite. Nach dem Registrieren wird das Login in der Datenbank gespeichert und man kann sich anschliessend einloggen. 

### 2. Aktien abfragen

Man kann beliebige Aktiensymbole, welche von yfinance unterstützt werden eingeben (z.B. aapl (Apple)). Danach schreibt man die Anzahl der Aktien die man gekauft hat und zu welchem Preis man diese gekauft hat und klickt auf Fertig. Sobald die Eingabe erfolgt, wird in yfinance der aktuelle Marktpreis abgefragt und die Rendite (Gewinn oder Verlust) ausgerechnet und angezeigt. Zusätzlich wird der Apple Preis der letzten 7 Tage mittels eines Plotly Liniendiagramm angezeigt. Yfinance und plotly wurden gewählt, da diese für Anfänger einfach implementierbar sind.

### 3. Zukünftige Erweiterungen

Das langfristige Ziel der Webapp ist es, dass mehrere Aktien unter den Profilen gespeichert werden können. Danach sollte man mit einem Kreisdiagramm den gesamten Wert der Aktien sehen und wieviel Prozent der Portfolios in welche Aktien investiert ist.

## Installation des Programms

Siehe installation.txt

## Quellen

Hintergrund (prog2/project1/static/bg.jpg): https://pixabay.com/de/photos/business-chart-graph-graphic-5475664/

Plotly Dokumentation: https://plotly.com/python/line-charts/

Plotly und flask:https://towardsdatascience.com/web-visualization-with-plotly-and-flask-3660abf9c946

Yfinance Dokumentation: https://python-yahoofinance.readthedocs.io/en/latest/

Yfinance andere Quellen: https://algotrading101.com/learn/yfinance-guide/, https://pypi.org/project/yfinance/, https://analyticsindiamag.com/hands-on-guide-to-using-yfinance-api-in-python/

Bootstrap Dokumentation: https://getbootstrap.com/, https://www.w3schools.com/bootstrap4/

Flask Dokumentation: https://flask.palletsprojects.com/en/2.0.x/

Flask-Login Dokumentation: https://flask-login.readthedocs.io/en/latest/

Flask-SQLAlchemy: https://flask-sqlalchemy.palletsprojects.com/en/2.x/

Jinja2: https://jinja.palletsprojects.com/en/3.0.x/, https://jinja2docs.readthedocs.io/en/stable/

graphJSON: https://www.graphjson.com/