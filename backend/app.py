from flask import Flask  # Flask-Framework importieren, um die Webanwendung zu erstellen
from flask_cors import CORS  # CORS (Cross-Origin Resource Sharing) importieren, um externe Anfragen zuzulassen
from catch import catch_blueprint  # Blueprint "catch" importieren, um modularen Code zu verwenden

# Erstelle eine Flask-App-Instanz
app = Flask(__name__)

# CORS aktivieren, um Anfragen von anderen Domains (Cross-Origin) zu ermöglichen
CORS(app)

# Blueprint registrieren, um Routen und Logik aus der "catch"-Komponente modular hinzuzufügen
app.register_blueprint(catch_blueprint)

# Route für die Startseite definieren
@app.route('/')
def home():
    # Rückgabe einer Willkommensnachricht als Antwort auf Anfragen an "/"
    return "Welcome to FisherFritz API!"

# Hauptfunktion, um den Flask-Server zu starten
if __name__ == '__main__':
    # Flask-App im Debug-Modus starten
    # Debug-Modus ermöglicht das automatische Neustarten des Servers bei Codeänderungen
    app.run(debug=True)
