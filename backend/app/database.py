from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# URL de conexión
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "mysql+pymysql://maolro:beersp_db@localhost:3306/beersp_db"
)

# pool_pre_ping=True ayuda a mantener la conexión activa en entornos como Docker.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True
)

# Define cómo se crearán las sesiones individuales.
SessionLocal = sessionmaker(
    autocommit=False,  # La sesión no confirma automáticamente (requiere db.commit())
    autoflush=False,   # No guarda automáticamente
    bind=engine
)

# Esta es la clase base de la que heredarán todos tus modelos (UsuarioDB, etc.)
Base = declarative_base()

#Función generadora que abre y cierra la sesión de la base de datos
def get_db():
    db = SessionLocal() # INICIA la sesión
    try:
        yield db        # Cede la sesión al controlador/endpoint de FastAPI
    finally:
        db.close()      # CIERRA la sesión, garantizando la liberación de recursos