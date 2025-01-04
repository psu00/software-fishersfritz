from flask import Blueprint, request, jsonify

# Blueprint erstellen
catch_blueprint = Blueprint('catch', __name__)

# Dummy-Daten (zum Testen, später durch eine Datenbank ersetzt)
catches = []

# Route: Fänge hinzufügen
@catch_blueprint.route('/catch', methods=['POST'])
def add_catch():
    data = request.get_json()
    if not data or not all(key in data for key in ['species', 'weight']):
        return jsonify({"error": "Invalid data"}), 400

    # Neuen Fang hinzufügen
    catch_id = len(catches) + 1
    new_catch = {"id": catch_id, "species": data['species'], "weight": data['weight']}
    catches.append(new_catch)
    return jsonify({"message": "Catch added successfully", "catch": new_catch}), 201

# Route: Alle Fänge abrufen
@catch_blueprint.route('/catch', methods=['GET'])
def get_catches():
    return jsonify(catches)


def catch_data():
    return "Data has been caught"

