import sqlite3

# Verbindung zur SQLite-Datenbank herstellen (erstellt die Datei, falls sie nicht existiert)
conn = sqlite3.connect('fischerfritz.db')
cursor = conn.cursor()

# Tabelle für Fischarten mit erlaubten Jahreszeiten und Schonzeiten erstellen
cursor.execute('''
CREATE TABLE IF NOT EXISTS fish (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    allowed_seasons TEXT NOT NULL,
    closed_season TEXT
)
''')

# Beispiel-Daten für die Fischarten hinzufügen
fish_list = [
    ("Rotauge", "Frühling,Sommer", None),  # Keine spezifische Schonzeit gefunden
    ("Brachse", "Frühling,Sommer,Herbst", None),  # Keine spezifische Schonzeit gefunden
    ("Hecht", "Ganzjährig", "01.01. - 30.04."),
    ("Karpfen", "Sommer,Herbst", "16.05. - 30.06."),
    ("Zander", "Ganzjährig", "01.01. - 31.05."),
    ("Wels", "Sommer", "15.05. - 15.07."),
    ("Flussbarsch", "Ganzjährig", None),  # Keine spezifische Schonzeit gefunden
    ("Schleie", "Frühling,Sommer", "01.06. - 30.06."),
    ("Reinanke", "Sommer", "01.11. - 28.02."),
    ("Seeforelle", "Herbst", "01.10. - 28.02.")
]

# Daten nur einfügen, wenn die Tabelle leer ist
cursor.execute('SELECT COUNT(*) FROM fish')
if cursor.fetchone()[0] == 0:
    cursor.executemany('INSERT INTO fish (name, allowed_seasons, closed_season) VALUES (?, ?, ?)', fish_list)
    print("Fischarten mit Schonzeiten wurden in die Datenbank eingefügt.")

# Änderungen speichern und Verbindung schließen
conn.commit()
conn.close()

print("Datenbank wurde erfolgreich eingerichtet und ist einsatzbereit.")