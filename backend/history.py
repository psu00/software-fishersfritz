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


 # Endpunkt: Alle Einträge anzeigen
@history_blueprint.route('/history', methods=['GET'])
def get_history():
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500

        # Abrufen aller Datensätze aus der Catch-Tabelle
        entries = conn.execute('SELECT * FROM catches').fetchall()
        conn.close()

        # Umwandeln der Ergebnisse in eine Liste von Dictionaries
        result = [dict(entry) for entry in entries]
        return jsonify(result), 200

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return jsonify({"error": "Database error", "details": str(e)}), 500   
