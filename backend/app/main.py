from flask import Flask, jsonify, g 
from flask_cors import CORS

from app.base_datos import SessionLocal, init_db
from app.controladores.cerveza_controlador import cerveza_bp
from app.controladores.galardon_controlador import galardon_bp
from app.controladores.usuario_controlador import usuario_bp
from app.controladores.degustacion_controlador import degustacion_bp
from app.controladores.cerveceria_controlador import cerveceria_bp

# --- Configuración de la App ---
app = Flask(__name__)
CORS(app)

@app.before_request
def get_db_session():
    """
    Se ejecuta ANTES de cada petición.
    Crea una sesión de BD única para esta petición y la guarda en 'g'.
    'g' es un objeto temporal de Flask.
    """
    g.db = SessionLocal() # Llama a la "fábrica" para crear una sesión

@app.teardown_request
def close_db_session(exception=None):
    """
    Se ejecuta DESPUÉS de cada petición, incluso si hay un error.
    Cierra la sesión de la BD para liberar la conexión.
    """
    db = g.pop('db', None) # Saca la sesión de 'g'
    if db is not None:
        db.close() # Cierra la sesión (¡muy importante!)

# --- Registro del Blueprint ---
# Le decimos a la app que use todas las rutas de los controladores
# y que todas ellas empiecen por "/api"
app.register_blueprint(cerveza_bp, url_prefix='/api')
app.register_blueprint(galardon_bp, url_prefix='/api')
app.register_blueprint(usuario_bp, url_prefix='/api')
app.register_blueprint(degustacion_bp, url_prefix='/api')
app.register_blueprint(cerveceria_bp, url_prefix='/api')

# --- Ruta de prueba (la que tenías) ---
@app.route("/")
def home():
    return jsonify(message="Hello from Python backend!")

# --- Arranque de la aplicación ---
if __name__ == "__main__":
    
    ### AÑADIDO: Inicializamos la BD y las tablas ###
    print("Inicializando la base de datos...")
    init_db()
    print("Base de datos lista.")
    
    print("\n--- Servidor listo. Rutas de API disponibles en: ---")
    print("--- USUARIOS ---")
    print(f"POST   http://localhost:8000/api/usuarios/")
    print(f"GET    http://localhost:8000/api/usuarios/")
    print(f"GET    http://localhost:8000/api/usuarios/<id>/")
    print(f"GET    http://localhost:8000/api/usuarios/<id>/amigos/")
    print(f"GET    http://localhost:8000/api/usuarios/<id>/amigos/<id>/")
    print("--- CERVEZAS ---")
    print(f"POST   http://localhost:8000/api/cervezas/")
    print(f"GET    http://localhost:8000/api/cervezas/")
    print(f"GET    http://localhost:8000/api/cervezas/<id>/")
    print(f"GET    http://localhost:8000/api/cervezas/estilos/")
    print("--- GALARDONES ---")
    print(f"POST   http://localhost:8000/api/galardones/")
    print(f"GET   http://localhost:8000/api/galardones/")
    print(f"GET    http://localhost:8000/api/galardones/<id>/")
    print(f"GET    http://localhost:8000/api/usuarios/<id>/galardones")
    print(f"GET    http://localhost:8000/api/usuarios/<id>/galardones/<id>")
    print("--- CERVECERÍAS ---")
    print(f"POST   http://localhost:8000/api/cervecerias/")
    print(f"GET   http://localhost:8000/api/cervecerias/")
    print(f"GET    http://localhost:8000/api/cervecerias/<id>/")
    print("--- DEGUSTACIONES ---")
    print(f"POST   http://localhost:8000/api/degustaciones/")
    print(f"GET   http://localhost:8000/api/degustaciones/")
    print(f"GET    http://localhost:8000/api/degustaciones/<id>/")
    print("...")
    
    app.run(host="0.0.0.0", port=8000, debug=True) # Añadido debug=True
