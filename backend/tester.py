from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from datetime import date
from uuid import uuid4

# --- Importaciones de tu proyecto ---
# Asumiendo que esta es la estructura de tu proyecto y que pytest se ejecuta desde la raíz 'backend/'
from app.database import Base, get_db
from app.controladores.usuario_controlador import usuario_router

# --- Configuración de la App de Prueba ---
app = FastAPI()
app.include_router(usuario_router)

# Creamos un cliente de prueba que "habla" con nuestra app
client = TestClient(app)

# --- Tests para cada Endpoint ---

def test_create_user(username: str, email: str, password: str, birth_date: date):
    """Prueba crear un usuario nuevo (POST /usuarios/)"""
    user_data = {
        "username": username,
        "email": email,
        "password": password,
        "birth_date": birth_date
    }
    
    response = client.post("/usuarios/", json=user_data)
    print(response.json())

def test_get_all_users():
    """Prueba obtener todos los usuarios (GET /usuarios/)"""
    response = client.get("/usuarios/")
    print(response.json())

def test_get_user(user_id: int):
    """
    Prueba el endpoint GET /{user_id} 
    """
    response = client.get(f"/usuarios/{user_id}")
    print(response.json())

def test_update_user(user_id: int, username: str, birth_date: str,
    email: str, password: str, friend: list):
    """Prueba actualizar un usuario (PUT /{user_id})"""  
    # Datos para actualizar (usando el modelo 'Usuario' Pydantic)
    update_data = {
        "id": user_id,
        "username": username, # Nuevo username
        "birth_date": birth_date,
        "email": email, # Mismo email
        "password": "newpass",
        "friends": ["friend1"]
    }

    response = client.put(f"/usuarios/{user_id}", json=update_data)
    print(response.json())

def test_delete_user(user_id: int):
    """Prueba eliminar un usuario (DELETE /{user_id})"""
    # Eliminamos el usuario
    delete_response = client.delete(f"/usuarios/{user_id}")
    # Imprime resultados
    print(delete_response.json())



# PRUEBAS
#test_delete_user(5)
#test_create_user("testuser", "test3@example.com", "pwd123", "2000-01-01")
test_get_user(6)
test_get_user(1)
test_get_user(2)
test_get_user(4)
test_get_all_users()

