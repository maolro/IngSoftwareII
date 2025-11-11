import sys
from sqlalchemy import create_engine, Column, Integer, String, Float, func, distinct
from sqlalchemy.orm import declarative_base, sessionmaker, Session
import logging

# --- CONFIGURACIÓN BÁSICA ---
# Desactivamos los logs de SQL para que la salida esté limpia
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.ERROR)

# --- 1. COPIAMOS TUS MODELOS Y SERVICIOS AQUÍ ---
# (Para que este script sea autoejecutable)

# --- Base ---
Base = declarative_base()

# --- Modelo Cerveza ---
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

# --- Servicio Cerveza ---
class CervezaService:
    @staticmethod
    def crear_cerveza(db: Session, cerveza_data: dict) -> Cerveza:
        db_cerveza_existente = db.query(Cerveza).filter(
            func.lower(Cerveza.nombre) == func.lower(cerveza_data['nombre'])
        ).first()
        if db_cerveza_existente:
            raise ValueError(f"La cerveza '{cerveza_data['nombre']}' ya existe.")
        
        atributos_modelo = Cerveza.__table__.columns.keys()
        data_limpia = {k: v for k, v in cerveza_data.items() if k in atributos_modelo}
        
        db_cerveza = Cerveza(**data_limpia)
        db.add(db_cerveza)
        db.commit()
        db.refresh(db_cerveza)
        return db_cerveza

    @staticmethod
    def buscar_cervezas(db: Session, q: str = None, estilo: str = None, pais: str = None) -> list[Cerveza]:
        query = db.query(Cerveza)
        if q:
            query = query.filter(Cerveza.nombre.ilike(f"%{q}%"))
        if estilo:
            query = query.filter(Cerveza.estilo == estilo)
        if pais:
            query = query.filter(Cerveza.pais_procedencia == pais)
        return query.order_by(Cerveza.nombre).all()

    @staticmethod
    def get_cerveza_por_id(db: Session, cerveza_id: int) -> Cerveza | None:
        return db.query(Cerveza).filter(Cerveza.id == cerveza_id).first()

    @staticmethod
    def get_valoracion_promedio(db: Session, cerveza_id: int) -> float:
        # Placeholder
        return 0.0 

    @staticmethod
    def get_favoritas_usuario(db: Session, usuario_id: int) -> list[dict]:
        # Placeholder
        return [
            {"id": 1, "nombre": "Cerveza Favorita 1 (Ejemplo)", "estilo": "IPA", "valoracion_usuario": 5.0},
        ]

    @staticmethod
    def get_estilos_unicos(db: Session) -> list[str]:
        query = db.query(distinct(Cerveza.estilo)).order_by(Cerveza.estilo)
        return [estilo[0] for estilo in query.all() if estilo[0]]

    @staticmethod
    def get_paises_unicos(db: Session) -> list[str]:
        query = db.query(distinct(Cerveza.pais_procedencia)).order_by(Cerveza.pais_procedencia)
        return [pais[0] for pais in query.all() if pais[0]]


# --- 2. CONFIGURACIÓN DE LA BASE DE DATOS DE PRUEBA (EN MEMORIA) ---

# Usamos ':memory:' para crear una BD temporal que se borra al acabar
engine = create_engine("sqlite:///:memory:")

# Creamos la tabla 'cervezas' en esta BD en memoria
Base.metadata.create_all(engine)

# Creamos la fábrica de sesiones
SessionLocal = sessionmaker(bind=engine)

# --- 3. SCRIPT DE PRUEBAS ---
print("--- 🚀 INICIANDO PRUEBAS DEL CervezaService ---")

# 'db' será nuestra conexión a la BD en memoria
db = SessionLocal()

try:
    # --- PREPARACIÓN: Añadimos datos de prueba ---
    print("\n[Paso 0] Añadiendo datos de prueba (seeds)...")
    CervezaService.crear_cerveza(db, {"nombre": "Mahou 5 Estrellas", "estilo": "Lager", "pais_procedencia": "España"})
    CervezaService.crear_cerveza(db, {"nombre": "Guinness Draught", "estilo": "Stout", "pais_procedencia": "Irlanda"})
    CervezaService.crear_cerveza(db, {"nombre": "Lagunitas IPA", "estilo": "IPA", "pais_procedencia": "EE.UU."})
    print("... Datos añadidos.")

    # --- PRUEBA 1: crear_cerveza (Duplicado) ---
    print("\n[Prueba 1] Intentando crear cerveza duplicada (debe fallar)...")
    try:
        CervezaService.crear_cerveza(db, {"nombre": "Mahou 5 Estrellas"})
        print("   ... ❌ ERROR: Debería haber fallado pero no lo hizo.")
    except ValueError as e:
        print(f"   ... ✅ ÉXITO: Error capturado como se esperaba: '{e}'")

    # --- PRUEBA 2: get_cerveza_por_id (Encontrado) ---
    print("\n[Prueba 2] Buscando cerveza con ID=2 (Guinness)...")
    cerveza = CervezaService.get_cerveza_por_id(db, 2)
    assert cerveza.nombre == "Guinness Draught"
    print(f"   ... ✅ ÉXITO: Encontrada: {cerveza.nombre}")

    # --- PRUEBA 3: get_cerveza_por_id (No Encontrado) ---
    print("\n[Prueba 3] Buscando cerveza con ID=99 (No existe)...")
    cerveza = CervezaService.get_cerveza_por_id(db, 99)
    assert cerveza is None
    print(f"   ... ✅ ÉXITO: Devuelve 'None' como se esperaba.")

    # --- PRUEBA 4: buscar_cervezas (Filtro por nombre 'q') ---
    print("\n[Prueba 4] Buscando cervezas que contengan 'ipa' (ignora mayús)...")
    resultados = CervezaService.buscar_cervezas(db, q="ipa")
    assert len(resultados) == 1
    assert resultados[0].nombre == "Lagunitas IPA"
    print(f"   ... ✅ ÉXITO: Encontrada 1 cerveza: {resultados[0].nombre}")

    # --- PRUEBA 5: buscar_cervezas (Filtro por estilo) ---
    print("\n[Prueba 5] Buscando cervezas de estilo 'Lager'...")
    resultados = CervezaService.buscar_cervezas(db, estilo="Lager")
    assert len(resultados) == 1
    assert resultados[0].nombre == "Mahou 5 Estrellas"
    print(f"   ... ✅ ÉXITO: Encontrada 1 cerveza: {resultados[0].nombre}")

    # --- PRUEBA 6: buscar_cervezas (Filtro por país) ---
    print("\n[Prueba 6] Buscando cervezas de país 'Irlanda'...")
    resultados = CervezaService.buscar_cervezas(db, pais="Irlanda")
    assert len(resultados) == 1
    assert resultados[0].nombre == "Guinness Draught"
    print(f"   ... ✅ ÉXITO: Encontrada 1 cerveza: {resultados[0].nombre}")

    # --- PRUEBA 7: buscar_cervezas (Sin filtros, todas) ---
    print("\n[Prueba 7] Buscando todas las cervezas (3)...")
    resultados = CervezaService.buscar_cervezas(db)
    assert len(resultados) == 3
    print(f"   ... ✅ ÉXITO: Encontradas {len(resultados)} cervezas.")

    # --- PRUEBA 8: get_estilos_unicos ---
    print("\n[Prueba 8] Obteniendo estilos únicos...")
    estilos = CervezaService.get_estilos_unicos(db)
    assert estilos == ["IPA", "Lager", "Stout"] # Vienen ordenados
    print(f"   ... ✅ ÉXITO: Estilos: {estilos}")

    # --- PRUEBA 9: get_paises_unicos ---
    print("\n[Prueba 9] Obteniendo países únicos...")
    paises = CervezaService.get_paises_unicos(db)
    assert paises == ["EE.UU.", "España", "Irlanda"] # Vienen ordenados
    print(f"   ... ✅ ÉXITO: Países: {paises}")

    # --- PRUEBA 10: Placeholders ---
    print("\n[Prueba 10] Probando placeholders (valoración y favoritas)...")
    valoracion = CervezaService.get_valoracion_promedio(db, 1)
    assert valoracion == 0.0
    favoritas = CervezaService.get_favoritas_usuario(db, 1)
    assert len(favoritas) > 0
    print(f"   ... ✅ ÉXITO: Placeholders devuelven valores de ejemplo.")

    print("\n--- ✅ ¡TODAS LAS PRUEBAS PASARON! ---")

except AssertionError as e:
    # `assert` falla, imprime el error
    print(f"\n--- ❌ PRUEBA FALLIDA ---")
    print(f"Error: La comprobación (assert) ha fallado.")
    # Imprime detalles del error (línea exacta)
    _, _, tb = sys.exc_info()
    print(f"Línea del error: {tb.tb_lineno}")
    
except Exception as e:
    # Otro error inesperado
    print(f"\n--- 💥 ERROR INESPERADO ---")
    print(f"Error: {e}")

finally:
    # Cerramos la conexión a la BD en memoria
    db.close()
    print("--- 🏁 PRUEBAS FINALIZADAS (BD en memoria cerrada) ---")