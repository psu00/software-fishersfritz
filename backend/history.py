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
           

 # Endpunkt: Gruppierte Fänge basierend auf Filter anzeingen (nach Fischart oder Datum)
@history_blueprint.route('/history/filter', methods=['GET'])
def filter_history():
    # Zeitraum aus Query-Parametern abrufen (z. B. "1day", "1week")
    filter_period = request.args.get('period', 'total')  # Standard: "total"

    try:
        conn = get_db_connection()
        filter_clause = ""  # Filter für den Zeitraum
        params = []

        # Zeitraum-Filter hinzufügen
        if filter_period == '1day':
            filter_clause = "WHERE date >= ?"
            params.append((datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'))
        elif filter_period == '1week':
            filter_clause = "WHERE date >= ?"
            params.append((datetime.now() - timedelta(weeks=1)).strftime('%Y-%m-%d'))
        elif filter_period == '1month':
            filter_clause = "WHERE date >= ?"
            params.append((datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'))
        elif filter_period == '1year':
            filter_clause = "WHERE date >= ?"
            params.append((datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d'))

        # Gruppierung nach Fischart
        query_by_fish = f"""
            SELECT fish_name, COUNT(*) AS count
            FROM catches
            {filter_clause}
            GROUP BY fish_name
            ORDER BY count DESC
        """
        grouped_by_fish = conn.execute(query_by_fish, params).fetchall()

        # Gruppierung nach Datum
        query_by_date = f"""
            SELECT date, fish_name, weight
            FROM catches
            {filter_clause}
            ORDER BY date ASC
        """
        grouped_by_date = conn.execute(query_by_date, params).fetchall()

        conn.close()

        # Ergebnisse formatieren
        result = {
            "by_fish": [dict(row) for row in grouped_by_fish],
            "by_date": {}
        }

        # Gruppieren nach Datum
        for row in grouped_by_date:
            date = row["date"]
            if date not in result["by_date"]:
                result["by_date"][date] = []
            result["by_date"][date].append({"fish_name": row["fish_name"], "weight": row["weight"]})

        return jsonify(result), 200

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