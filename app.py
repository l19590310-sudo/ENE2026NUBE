import os
from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
app.secret_key = "clave_secreta_segura"

# ==========================
# Configuración Base de Datos
# ==========================
database_url = os.getenv('DATABASE_URL')

if database_url:
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///skincare.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ==========================
# Modelo Skincare
# ==========================
class Producto(db.Model):
    __tablename__ = 'productos_skincare'

    id_producto = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    marca = db.Column(db.String(100), nullable=False)
    tipo_producto = db.Column(db.String(50), nullable=False)
    tipo_piel = db.Column(db.String(50), nullable=False)
    precio = db.Column(db.Float, nullable=False)

# Crear tablas automáticamente
with app.app_context():
    db.create_all()

# ==========================
# Rutas
# ==========================

@app.route('/')
@app.route('/productos')
def index():
    productos = Producto.query.all()
    return render_template('index.html', productos=productos)

@app.route('/productos/new', methods=['GET', 'POST'])
def create_producto():
    if request.method == 'POST':
        nuevo = Producto(
            nombre=request.form['nombre'],
            marca=request.form['marca'],
            tipo_producto=request.form['tipo_producto'],
            tipo_piel=request.form['tipo_piel'],
            precio=float(request.form['precio'])
        )

        db.session.add(nuevo)
        db.session.commit()

        flash('Producto agregado correctamente', 'success')
        return redirect(url_for('index'))

    return render_template('create_producto.html')

@app.route('/productos/update/<int:id_producto>', methods=['GET', 'POST'])
def update_producto(id_producto):
    producto = Producto.query.get_or_404(id_producto)

    if request.method == 'POST':
        producto.nombre = request.form['nombre']
        producto.marca = request.form['marca']
        producto.tipo_producto = request.form['tipo_producto']
        producto.tipo_piel = request.form['tipo_piel']
        producto.precio = float(request.form['precio'])

        db.session.commit()
        flash('Producto actualizado correctamente', 'info')
        return redirect(url_for('index'))

    return render_template('update_producto.html', producto=producto)

@app.route('/productos/delete/<int:id_producto>')
def delete_producto(id_producto):
    producto = Producto.query.get_or_404(id_producto)

    db.session.delete(producto)
    db.session.commit()

    flash('Producto eliminado correctamente', 'danger')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)