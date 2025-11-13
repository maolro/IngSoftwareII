from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

# --- Esquemas para Galardon (Definición del galardón) ---

class GalardonBase(BaseModel):
    nombre: str
    descripcion: str
    imagen_url: Optional[str] = None
    tipo: str # 'cantidad_cervezas', 'pais', 'comentarios'
    condiciones: Optional[Dict[str, Any]] = None # {"niveles": [5, 10, 25]}

# Esquema para crear un nuevo tipo de galardón (RF-4.5)
class GalardonCreate(GalardonBase):
    pass

# Esquema para leer/devolver un galardón
class Galardon(GalardonBase):
    id: int

    class Config:
        # Permite que Pydantic lea los modelos de SQLAlchemy
        orm_mode = True 

# --- Esquemas para UsuarioGalardon (El galardón que tiene un usuario) ---

# Esquema para devolver el galardón de un usuario con detalles
class UsuarioGalardonDetalle(BaseModel):
    nivel_actual: int
    progreso_actual: int
    obtenido_en: datetime
    galardon: Galardon # Anidamos la info del galardón

    class Config:
        orm_mode = True
