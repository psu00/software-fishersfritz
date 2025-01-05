from flask import Flask, Blueprint, request, jsonify
from flask_cors import CORS  # Cross-Origin Resource Sharing wird importiert, um API-Zugriffe von verschiedenen Domains zu ermöglichen

# Blueprint erstellen
# Blueprints dienen dazu, Routen und Logik modular zu organisieren und macht eine trennung in app.py, history.py und catch.py möglich
catch_blueprint = Blueprint('catch', __name__)

def get_db_connection():
    # Importieren des SQLite-Moduls innerhalb der Funktion, um Abhängigkeiten lokal zu halten.
    import sqlite3  # SQLite-Datenbankmodul wird importiert
    conn = sqlite3.connect('fischerfritz.db')  # Verbindung zur SQLite-Datenbank wird hergestellt
    conn.row_factory = sqlite3.Row  # Konfiguriert die Rückgabewerte so, dass sie wie Dictionaries aussehen
    return conn  # Gibt die Datenbankverbindung zurück

# Route: Fang hinzufügen
@catch_blueprint.route('/catch', methods=['POST'])  # POST-Methode, um neue Daten zu senden
def add_catch():
    # JSON-Daten aus der Anfrage auslesen
    new_catch = request.get_json()
    # Extrahieren der einzelnen Felder aus dem JSON-Objekt
    fish_name = new_catch.get('fish_name')
    latitude = new_catch.get('latitude')
    longitude = new_catch.get('longitude')
    weight = new_catch.get('weight')
    date = new_catch.get('date')
    # Validierung: Überprüfung, ob alle erforderlichen Felder vorhanden sind
    if not (fish_name and longitude and latitude and weight and date):
        return jsonify({"error": "Missing required fields"}), 400  # Fehlermeldung mit HTTP-Statuscode 400 (Bad Request)
    # Verbindung zur Datenbank herstellen
    conn = get_db_connection()
    # SQL-Query zur Einfügung eines neuen Eintrags in die Tabelle "catches"
    conn.execute(
        'INSERT INTO catches (fish_name, longitude, latitude, weight, date) VALUES (?, ?, ?, ?, ?)',
        (fish_name, longitude, latitude, weight, date)
    )
    conn.commit()  # Änderungen speichern
    conn.close()  # Datenbankverbindung schließen
    return jsonify({"message": "Catch added successfully"}), 201  # Erfolgsnachricht mit HTTP-Statuscode 201 (Created)

# Placeholder-Funktion (dient keinem direkten Zweck im aktuellen Kontext)
def catch_data():
    return "Data has been caught"
