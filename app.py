from flask import Flask, render_template, request, jsonify, send_file
import sqlite3
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)

DB_NAME = 'database.db'

# Ruta principal
@app.route('/')
def index():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ventas")
    ventas = cursor.fetchall()
    conn.close()
    return render_template('index.html', ventas=ventas)

# Agregar producto
@app.route('/agregar', methods=['POST'])
def agregar():
    producto = request.form['producto']
    cantidad = int(request.form['cantidad'])
    precio = float(request.form['precio'])
    total = cantidad * precio

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ventas (producto, cantidad, precio, total) VALUES (?, ?, ?, ?)",
                   (producto, cantidad, precio, total))
    conn.commit()
    conn.close()

    return jsonify({'mensaje': 'Producto agregado correctamente'})

# Generar reporte
@app.route('/reporte')
def reporte():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM ventas", conn)
    conn.close()

    fecha = datetime.now().strftime("%Y-%m-%d")
    nombre_archivo = f"reporte_ventas_{fecha}.xlsx"
    df.to_excel(nombre_archivo, index=False)

    return send_file(nombre_archivo, as_attachment=True)

# Finalizar día
@app.route('/finalizar', methods=['POST'])
def finalizar():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ventas")
    conn.commit()
    conn.close()
    return jsonify({'mensaje': 'Día finalizado, datos borrados'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
