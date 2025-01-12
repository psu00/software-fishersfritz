from flask import Blueprint, jsonify
import sqlite3

fish_blueprint = Blueprint('fish', __name__)

def get_db_connection():
    conn = sqlite3.connect('fischerfritz.db')
    conn.row_factory = sqlite3.Row
    return conn

@fish_blueprint.route('/fish', methods=['GET'])
def get_fish_names():
    try:
        conn = get_db_connection()
        fish_names = conn.execute("SELECT name FROM fish").fetchall()
        conn.close()
        return jsonify([fish['name'] for fish in fish_names]), 200
    except sqlite3.Error as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500
