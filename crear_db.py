import sqlite3

# Conexión a la base de datos
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Crear tabla
cursor.execute('''
CREATE TABLE IF NOT EXISTS ventas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    producto TEXT NOT NULL,
    cantidad INTEGER NOT NULL,
    precio REAL NOT NULL,
    total REAL NOT NULL
)
''')

print("Base de datos creada correctamente ✅")
conn.commit()
conn.close()
