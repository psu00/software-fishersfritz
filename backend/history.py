from flask import Blueprint, request, jsonify
from flask_cors import CORS  # Cross-Origin Resource Sharing wird importiert, um API-Zugriffe von verschiedenen Domains zu ermöglichen
from datetime import datetime, timedelta # Importieren des datetime-Moduls, um Datums- und Zeitfunktionen zu verwenden
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

 # Endpunkt: Gruppierte Fänge basierend auf Zeiträumen
@history_blueprint.route('/history/filter', methods=['GET'])
def filter_history():
    # Zeitraum aus Query-Parametern abrufen (z. B. "1day", "1week")
    filter_period = request.args.get('period', 'total')  # Default: "total"

    try:
        conn = get_db_connection()
        query = """
            SELECT fish_name, COUNT(*) AS count
            FROM catches
        """
        params = []

        # Zeitraum-Filter hinzufügen
        if filter_period == '1day':
            query += " WHERE date >= ?"
            params.append((datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'))
        elif filter_period == '1week':
            query += " WHERE date >= ?"
            params.append((datetime.now() - timedelta(weeks=1)).strftime('%Y-%m-%d'))
        elif filter_period == '1month':
            query += " WHERE date >= ?"
            params.append((datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'))
        elif filter_period == '1year':
            query += " WHERE date >= ?"
            params.append((datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d'))

        # Gruppierung und Sortierung hinzufügen
        query += " GROUP BY fish_name ORDER BY count DESC"

        # Query ausführen
        result = conn.execute(query, params).fetchall()
        conn.close()

        # Ergebnisse als Liste von Dictionaries zurückgeben
        grouped_data = [dict(row) for row in result]
        return jsonify(grouped_data), 200

    except sqlite3.Error as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500

 # Endpunkt: Eintrag löschen
@history_blueprint.route('/history/<int:catch_id>', methods=['DELETE'])
def delete_history(catch_id):
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500

        # Löschen des Eintrags
        conn.execute('DELETE FROM catches WHERE id = ?', (catch_id,))
        conn.commit()
        conn.close()

        return jsonify({"message": "Catch deleted successfully"}), 200

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return jsonify({"error": "Database error", "details": str(e)}), 500