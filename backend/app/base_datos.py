import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import StaticPool

# ACCEDER SQLITE: sqlite3 database.db

# --- Configuración de la Base de Datos ---

# Usamos una base de datos SQLite en un archivo.
# La ruta ahora apuntará al directorio 'app'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"

# Creamos el "motor" de la base de datos
engine = create_engine(
    DATABASE_URL,
    # Esta configuración es necesaria para que SQLite funcione bien con Flask
    connect_args={"check_same_thread": False},
    # StaticPool es recomendado por FastAPI/Flask para SQLite
    poolclass=StaticPool
)

# Creamos una 'fábrica' de sesiones de base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 'Base' es la clase de la que heredarán todos nuestros modelos (objetos)
Base = declarative_base()

# --- Función para crear la base de datos ---
def init_db():
    """
    Inicializa la base de datos y crea las tablas si no existen.
    """
    # Importamos los modelos aquí para que 'Base' los reconozca
    # ¡Tendrás que importar aquí todos tus modelos!
    from .objetos import usuario, cerveza, galardon
    # from .objetos import degustacion # (Cuando tu compañero lo cree)
    
    print(f"Creando tablas en la base de datos en: {DB_PATH}")

    # Deputación para ver tablas creadas
    print("Tablas a crear:")
    for table_name, table in Base.metadata.tables.items():
        print(f"   - {table_name}")

    Base.metadata.create_all(bind=engine)
    print("Tablas creadas exitosamente.")

# --- Función para obtener una sesión  ---
def get_db():
    """
    Función helper para obtener una sesión de base de datos.
    Esto se usará en app.py (con g.db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()