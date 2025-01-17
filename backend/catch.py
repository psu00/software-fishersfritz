from flask import Flask, Blueprint, request, jsonify
from flask_cors import CORS  # Cross-Origin Resource Sharing wird importiert, um API-Zugriffe von verschiedenen Domains zu ermöglichen
from datetime import datetime # Importieren des datetime-Moduls, um Datums- und Zeitfunktionen zu verwenden
import sqlite3  # Importieren des SQLite-Moduls, um mit der SQLite-Datenbank zu interagieren

# Blueprint erstellen
# Blueprints dienen dazu, Routen und Logik modular zu organisieren und macht eine trennung in app.py, history.py und catch.py möglich
catch_blueprint = Blueprint('catch', __name__)

def get_db_connection():
    try:
        conn = sqlite3.connect('fischerfritz.db')  # Verbindung zur SQLite-Datenbank wird hergestellt
        conn.row_factory = sqlite3.Row  # Konfiguriert die Rückgabewerte so, dass sie wie Dictionaries aussehen
        return conn  # Gibt die Datenbankverbindung zurück
    except sqlite3.Error as e:
        print(f"SQLite Fehler: {e}")
        
        return jsonify({"error": "Database error", "details": str(e)}), 500

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
    length = new_catch.get('length')

    print(f"SQL: INSERT INTO catches (fish_name, longitude, latitude, weight, date, length)")
    print(f"Values: {fish_name}, {longitude}, {latitude}, {weight}, {date}, {length}")

    # Validierung: Überprüfung, ob alle erforderlichen Felder vorhanden sind
    if not (fish_name and longitude and latitude and weight and date and length):
        return jsonify({"error": "Missing required fields"}), 400  # Fehlermeldung mit HTTP-Statuscode 400 (Bad Request)
    
    try:
        conn = get_db_connection() # Verbindung zur Datenbank herstellen


    # SQL-Query zur Überprüfung, ob die Fischart in der Datenbank vorhanden ist
        fish = conn.execute(
            'SELECT * FROM fish WHERE name = ?',
            (fish_name,)
        ).fetchone()

        if not fish:
        # Fehler: Fisch existiert nicht in der Tabelle
            print(f"Validation failed: Fish '{fish_name}' does not exist in fish table.")
            return jsonify({"error": f"Fish '{fish_name}' is not recognized."}), 400
        
        # Überprüfen, ob der Fisch gefangen werden darf
        if not fish['is_allowed']:
            print(f"Validation failed: Fish '{fish_name}' is not allowed to be caught.")
            return jsonify({"error": f"Fish '{fish_name}' is not allowed to be caught."}), 400
        
        # **Brittelmaß-Validierung**
        brittelmaß = fish['minimum_size_cm']
        if brittelmaß and float(length) < brittelmaß:
            print(f"Validation failed: Fish '{fish_name}' is smaller than the required minimum size ({brittelmaß} cm).")
            return jsonify({"error": f"Fish '{fish_name}' is smaller than the required minimum size ({brittelmaß} cm)."}), 400
        
        # Validierung: Überprüfung des Datumsformats
        try:
            # Versuche, das Datum zu parsen
            catch_date = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": f"Invalid date format: '{date}'. Expected format: YYYY-MM-DD"}), 400
        
        # Schonzeit-Validierung
        closed_season_start = fish['closed_season_start']
        closed_season_end = fish['closed_season_end']

        if closed_season_start and closed_season_end:
            # Konvertiere Schonzeit und Fangdatum
            catch_date = datetime.strptime(date, "%Y-%m-%d").date()  # Datum aus Anfrage
            year = catch_date.year  # Jahr des Fangdatums

            # Konvertiere Start- und Enddatum der Schonzeit in vollständige Datumswerte
            season_start = datetime.strptime(f"{year}-{closed_season_start}", "%Y-%m-%d").date()
            season_end = datetime.strptime(f"{year}-{closed_season_end}", "%Y-%m-%d").date()

            # Sonderfall: Jahreswechsel (z. B. 01.12. - 31.01.)
            if season_start > season_end:
                # Wenn die Schonzeit über den Jahreswechsel geht
                if not (catch_date >= season_start or catch_date <= season_end):
                    print(f"Validation failed: Catch date '{date}' is within the closed season for fish '{fish_name}'.")
                    return jsonify({"error": f"Fish '{fish_name}' cannot be caught during its closed season ({season_start} to {season_end})."}), 400 
            else:
                # Normale Schonzeit
                if season_start <= catch_date <= season_end:
                    print(f"Validation failed: Catch date '{date}' is within the closed season for fish '{fish_name}'.")
                    return jsonify({"error": f"Fish '{fish_name}' cannot be caught during its closed season ({season_start} to {season_end})."}), 400 
            if not closed_season_start or not closed_season_end:
                # Keine Schonzeit definiert, daher ist der Fang erlaubt
                season_start = None
                season_end = None
       
        # Validierung: Überprüfung, ob das Gewicht eine positive Zahl ist
        if float(weight) <= 0:
            return jsonify({"error": "Validation failed: Weight must be a positive number"}), 400  


        # SQL-Query zur Einfügung eines neuen Eintrags in die Tabelle "catches"
        conn.execute(
            'INSERT INTO catches (fish_name, longitude, latitude, weight, date, length) VALUES (?, ?, ?, ?, ?, ?)',
            (fish_name, longitude, latitude, weight, date, length)
        )
        conn.commit()  # Änderungen speichern
        conn.close()  # Datenbankverbindung schließen
        return jsonify({"message": "Catch added successfully"}), 201  # Erfolgsnachricht mit HTTP-Statuscode 201 (Created)

    except sqlite3.Error as e:
        # Fehlerprotokollierung
        print(f"Database error: {e}")
        return jsonify({"error": "Database error", "details": str(e)}), 500

# Placeholder-Funktion (dient keinem direkten Zweck im aktuellen Kontext)
def catch_data():
    return "Data has been caught"
