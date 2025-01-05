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

