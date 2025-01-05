from flask import Blueprint, request, jsonify
import sqlite3

# Blueprint für die "history"-Komponente erstellen
history_blueprint = Blueprint('history', __name__)

# Hilfsfunktion: Verbindung zur Datenbank herstellen
def get_db_connection():
    try:
        conn = sqlite3.connect('fischerfritz.db')  # SQLite-Datenbankverbindung
        conn.row_factory = sqlite3.Row  # Ergebnisse als Dictionary-like Objekte
        return conn
    except sqlite3.Error as e:
        print(f"SQLite Fehler: {e}")
        return None
    
