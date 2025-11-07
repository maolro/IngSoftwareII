from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# --- 1. CONFIGURACIÓN ---

# La Base de la que heredan tus modelos
Base = declarative_base()

# El "motor" que se conecta a tu archivo database.db
DATABASE_URL = "sqlite:///database.db"
engine = create_engine(DATABASE_URL)

# --- 2. TU MODELO (Lo pego aquí para que el script funcione solo) ---

class Cerveza(Base):
    __tablename__ = "cervezas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True, nullable=False)
    descripcion = Column(String)
    foto = Column(String)
    estilo = Column(String, index=True)
    pais_procedencia = Column(String, index=True)
    tamano = Column(String)
    formato = Column(String)
    porcentaje_alcohol = Column(Float)
    ibu = Column(Integer)
    color = Column(String)

# --- 3. CREAR LA TABLA (si no existe) ---
Base.metadata.create_all(bind=engine)
print("--- Tabla 'cervezas' comprobada/creada. ---")

# --- 4. CREAR LA SESIÓN (El "canal" de comunicación) ---
SessionLocal = sessionmaker(bind=engine)

# --- 5. PROGRAMA DE PRUEBAS ---
print("--- 🍺 Iniciando programa de pruebas ---")

# 'with' se encarga de abrir y cerrar la conexión automáticamente
with SessionLocal() as db:
    
    # --- PRUEBA 1: AÑADIR UNA CERVEZA ---
    print("\n1. Intentando añadir 'IPA Especial'...")
    
    cerveza_nueva = Cerveza(
        nombre="IPA Especial",
        estilo="India Pale Ale",
        porcentaje_alcohol=6.5,
        ibu=60,
        pais_procedencia="EE.UU."
    )
    
    # La añadimos a la "sala de espera" (sesión)
    db.add(cerveza_nueva)
    
    # Ahora, intentamos guardarla en la BD
    try:
        db.commit() # ¡Aquí es donde se guarda!
        print("   ... ¡'IPA Especial' guardada con éxito!")
        
    except Exception as e:
        db.rollback() # Si falla (ej: ya existe), deshace los cambios
        print(f"   ... ERROR: No se pudo guardar. (Quizás ya existe)")
        # print(f"   Error detallado: {e}") # Descomenta para ver el error

    # --- PRUEBA 2: LEER (Consultar) TODAS LAS CERVEZAS ---
    print("\n2. Consultando todas las cervezas en la base de datos:")
    
    # Pedimos a la BD todas las filas de la tabla Cerveza
    lista_cervezas = db.query(Cerveza).all()
    
    if not lista_cervezas:
        print("   ... No hay ninguna cerveza en la base de datos.")
    else:
        # Recorremos la lista y la imprimimos
        for cerveza in lista_cervezas:
            print(f"   - ID: {cerveza.id}, Nombre: {cerveza.nombre}, Estilo: {cerveza.estilo}")

print("\n--- 🏁 Pruebas finalizadas ---")