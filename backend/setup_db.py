import sqlite3

# Verbindung zur SQLite-Datenbank herstellen (erstellt die Datei, falls sie nicht existiert)
conn = sqlite3.connect('fischerfritz.db')
cursor = conn.cursor()

# Tabelle für dokumentierte Fänge erstellen
cursor.execute('''
CREATE TABLE IF NOT EXISTS catches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fish_name TEXT NOT NULL,
    latitude REAL,
    longitude REAL,
    weight REAL NOT NULL,
    date TEXT NOT NULL
)
''')

# Tabelle für Fischarten mit erlaubten Jahreszeiten und Schonzeiten erstellen
cursor.execute('''
CREATE TABLE IF NOT EXISTS fish (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    is_allowed BOOLEAN NOT NULL,
    closed_season_start TEXT,
    closed_season_end TEXT
)
''')

# Beispiel-Daten für die Fischarten hinzufügen
fish_list = [
    ("Rotauge", True, None, None),  # Keine spezifische Schonzeit
    ("Brachse", True, None, None),  # Keine spezifische Schonzeit
    ("Hecht", True, "01-01", "04-30"),
    ("Karpfen", True, "05-16", "06-30"),
    ("Zander", True, "01-01", "05-31"),
    ("Wels", True, "05-15", "07-15"),
    ("Flussbarsch", True, None, None),  # Keine spezifische Schonzeit
    ("Schleie", True, "06-01", "06-30"),
    ("Huchen", False, None, None),
    ("Reinanke", True, "11-01", "02-28"),
    ("Seeforelle", True, "10-01", "02-28")
]


# Daten nur einfügen, wenn die Tabelle leer ist
cursor.execute('SELECT COUNT(*) FROM fish')
if cursor.fetchone()[0] == 0:
    cursor.executemany('INSERT INTO fish (name, is_allowed, closed_season_start, closed_season_end) VALUES (?, ?, ?, ?)', fish_list)
    print("Fischarten mit Schonzeiten wurden in die Datenbank eingefügt.")

# Änderungen speichern und Verbindung schließen
conn.commit()
conn.close()

print("Datenbank wurde erfolgreich eingerichtet und ist einsatzbereit.")