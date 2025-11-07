from fastapi import FastAPI
from .database import Base, engine
from controladores.usuario_controlador import usuario_router

# Crea las tablas en la base de datos (si no existen)
Base.metadata.create_all(bind=engine)

# Inicializa la aplicación FastAPI
app = FastAPI(
    title="BeerSP API",
    description="Backend para la aplicación BeerSP.",
    version="1.0.0"
)

# Incluye el router de usuarios
app.include_router(usuario_router)

@app.get("/", tags=["Root"])
def read_root():
    """Endpoint raíz para verificar que la API está funcionando."""
    return {"message": "Bienvenido a la API de BeerSP. Visita /docs para la documentación."}
