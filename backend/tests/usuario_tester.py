from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from datetime import date
import time

# --- Importaciones de tu proyecto ---
from app.database import Base, get_db
from app.controladores.usuario_controlador import usuario_router

# --- Configuración de la App de Prueba ---
app = FastAPI()
app.include_router(usuario_router)
client = TestClient(app)

class UsuarioTester:
    """Clase para realizar pruebas automatizadas de los endpoints de usuarios"""
    
    def __init__(self):
        self.created_users = []  # Track users created during tests
        self.test_results = {
            'passed': 0,
            'failed': 0,
            'errors': []
        }
    
    def print_header(self, message):
        """Print a formatted header"""
        print(f"\n{'='*60}")
        print(f"{message}")
        print(f"{'='*60}")
    
    def print_success(self, message):
        """Print success message"""
        print(f"✅ {message}")
        self.test_results['passed'] += 1
    
    def print_error(self, message, error=None):
        """Print error message"""
        print(f"❌ {message}")
        if error:
            print(f"   Error: {error}")
        self.test_results['failed'] += 1
        self.test_results['errors'].append(message)
    
    def print_info(self, message):
        """Print info message"""
        print(f"\n{'='*60}\n")
        print(f"ℹ️  {message}")
    
    def wait_for_operation(self, seconds=1):
        """Wait between operations to avoid race conditions"""
        time.sleep(seconds)
    
    def test_create_user(self, username: str, email: str, password: str, birth_date: str, expected_success=True):
        """Prueba crear un usuario nuevo"""
        self.print_header(f"CREANDO USUARIO: {username}")
        
        user_data = {
            "username": username,
            "email": email,
            "password": password,
            "birth_date": birth_date
        }
        
        try:
            response = client.post("/usuarios/", json=user_data)
            result = response.json()
            
            print(f"Status Code: {response.status_code}")
            print(f"Response: {result}")
            
            if expected_success and response.status_code == 201:
                user_id = result.get('user_id')
                if user_id:
                    self.created_users.append(user_id)
                    self.print_success(f"Usuario '{username}' creado exitosamente con ID: {user_id}")
                    return user_id
                else:
                    self.print_error("Usuario creado pero no se recibió ID")
                    return None
            elif not expected_success and response.status_code != 201:
                self.print_success(f"Creación fallida como se esperaba: {result.get('detail', '')}")
                return None
            else:
                self.print_error(f"Resultado inesperado. Esperado éxito: {expected_success}")
                return None
                
        except Exception as e:
            self.print_error(f"Error creando usuario '{username}'", str(e))
            return None
    
    def test_get_user(self, user_id: int, expected_success=True):
        """Prueba obtener un usuario por ID"""
        self.print_header(f"OBTENIENDO USUARIO ID: {user_id}")
        
        try:
            response = client.get(f"/usuarios/{user_id}")
            result = response.json()
            
            print(f"Status Code: {response.status_code}")
            
            if expected_success and response.status_code == 200:
                self.print_success(f"Usuario obtenido: {result.get('username', 'N/A')}")
                return result
            elif not expected_success and response.status_code == 404:
                self.print_success("Usuario no encontrado (como se esperaba)")
                return None
            else:
                self.print_error(f"Resultado inesperado al obtener usuario {user_id}")
                return None
                
        except Exception as e:
            self.print_error(f"Error obteniendo usuario {user_id}", str(e))
            return None
    
    def test_get_all_users(self):
        """Prueba obtener todos los usuarios"""
        self.print_header("OBTENIENDO TODOS LOS USUARIOS")
        
        try:
            response = client.get("/usuarios/")
            result = response.json()
            
            print(f"Status Code: {response.status_code}")
            print(f"Total de usuarios: {len(result)}")
            
            if response.status_code == 200:
                self.print_success(f"Obtenidos {len(result)} usuarios exitosamente")
                return result
            else:
                self.print_error("Error obteniendo todos los usuarios")
                return None
                
        except Exception as e:
            self.print_error("Error obteniendo todos los usuarios", str(e))
            return None
    
    def test_update_user(self, user_id: int, username: str, email: str, birth_date: str, expected_success=True):
        """Prueba actualizar un usuario"""
        self.print_header(f"ACTUALIZANDO USUARIO ID: {user_id}")
        
        update_data = {
            "user_id": user_id,
            "username": username,
            "email": email,
            "birth_date": birth_date,
            "password": "updated_password",
            "friends": []
        }
        
        try:
            response = client.put(f"/usuarios/{user_id}", json=update_data)
            result = response.json()
            
            print(f"Status Code: {response.status_code}")
            print(f"Response: {result}")
            
            if expected_success and response.status_code == 200:
                if result.get('username') == username:
                    self.print_success(f"Usuario actualizado a: {username}")
                    return result
                else:
                    self.print_error("Usuario actualizado pero datos no coinciden")
                    return None
            elif not expected_success and response.status_code != 200:
                self.print_success("Actualización fallida como se esperaba")
                return None
            else:
                self.print_error("Resultado inesperado en actualización")
                return None
                
        except Exception as e:
            self.print_error(f"Error actualizando usuario {user_id}", str(e))
            return None
    
    def test_delete_user(self, user_id: int, expected_success=True):
        """Prueba eliminar un usuario"""
        self.print_header(f"ELIMINANDO USUARIO ID: {user_id}")
        
        try:
            response = client.delete(f"/usuarios/{user_id}")
            result = response.json()
            
            print(f"Status Code: {response.status_code}")
            print(f"Response: {result}")
            
            if expected_success and response.status_code == 200:
                self.print_success(f"Usuario {user_id} eliminado exitosamente")
                if user_id in self.created_users:
                    self.created_users.remove(user_id)
                return True
            elif not expected_success and response.status_code == 404:
                self.print_success("Eliminación fallida como se esperaba (usuario no existe)")
                return False
            else:
                self.print_error("Resultado inesperado en eliminación")
                return False
                
        except Exception as e:
            self.print_error(f"Error eliminando usuario {user_id}", str(e))
            return False
    
    def test_add_friend(self, user_id: int, friend_id: int, expected_success=True):
        """Prueba agregar un amigo"""
        self.print_header(f"AGREGANDO AMIGO: Usuario {user_id} -> Amigo {friend_id}")
        
        friend_request = {"friend_id": friend_id}
        
        try:
            response = client.post(f"/usuarios/{user_id}/amigos/", json=friend_request)
            result = response.json()
            
            print(f"Status Code: {response.status_code}")
            print(f"Response: {result}")
            
            if expected_success and response.status_code == 201 and result.get('success'):
                self.print_success(f"Amistad creada: {user_id} -> {friend_id}")
                return True
            elif not expected_success and (response.status_code != 201 or not result.get('success')):
                self.print_success("Amistad no creada (como se esperaba)")
                return False
            else:
                self.print_error("Resultado inesperado al agregar amigo")
                return False
                
        except Exception as e:
            self.print_error(f"Error agregando amigo {friend_id} a usuario {user_id}", str(e))
            return False
    
    def test_get_user_friends(self, user_id: int, expected_count=None):
        """Prueba obtener lista de amigos de un usuario"""
        self.print_header(f"OBTENIENDO AMIGOS DEL USUARIO {user_id}")
        
        try:
            response = client.get(f"/usuarios/{user_id}/amigos/")
            result = response.json()
            
            print(f"Status Code: {response.status_code}")
            print(f"Amigos encontrados: {len(result)}")
            
            if response.status_code == 200:
                if expected_count is None or len(result) == expected_count:
                    self.print_success(f"Obtenidos {len(result)} amigos exitosamente")
                    return result
                else:
                    self.print_error(f"Se esperaban {expected_count} amigos, se obtuvieron {len(result)}")
                    return result
            else:
                self.print_error("Error obteniendo amigos del usuario")
                return None
                
        except Exception as e:
            self.print_error(f"Error obteniendo amigos del usuario {user_id}", str(e))
            return None
    
    def test_get_friend_details(self, user_id: int, friend_id: int, expected_success=True):
        """Prueba obtener detalles de un amigo específico"""
        self.print_header(f"OBTENIENDO DETALLES DEL AMIGO {friend_id} PARA USUARIO {user_id}")
        
        try:
            response = client.get(f"/usuarios/{user_id}/amigos/{friend_id}")
            result = response.json()
            
            print(f"Status Code: {response.status_code}")
            
            if expected_success and response.status_code == 200:
                self.print_success(f"Detalles del amigo obtenidos: {result.get('username', 'N/A')}")
                return result
            elif not expected_success and response.status_code == 404:
                self.print_success("Amigo no encontrado (como se esperaba)")
                return None
            else:
                self.print_error("Resultado inesperado al obtener detalles del amigo")
                return None
                
        except Exception as e:
            self.print_error(f"Error obteniendo detalles del amigo {friend_id}", str(e))
            return None
    
    def test_remove_friend(self, user_id: int, friend_id: int, expected_success=True):
        """Prueba eliminar un amigo"""
        self.print_header(f"ELIMINANDO AMIGO: Usuario {user_id} -> Amigo {friend_id}")
        
        try:
            response = client.delete(f"/usuarios/{user_id}/amigos/{friend_id}")
            result = response.json()
            
            print(f"Status Code: {response.status_code}")
            print(f"Response: {result}")
            
            if expected_success and response.status_code == 200 and result.get('success'):
                self.print_success(f"Amigo {friend_id} eliminado exitosamente")
                return True
            elif not expected_success and (response.status_code != 200 or not result.get('success')):
                self.print_success("Amigo no eliminado (como se esperaba)")
                return False
            else:
                self.print_error("Resultado inesperado al eliminar amigo")
                return False
                
        except Exception as e:
            self.print_error(f"Error eliminando amigo {friend_id} del usuario {user_id}", str(e))
            return False
    
    def run_comprehensive_test(self):
        """Ejecuta una prueba completa de todos los endpoints"""
        self.print_header("INICIANDO PRUEBA COMPREHENSIVA")
        
        # Paso 1: Crear usuarios de prueba
        self.print_info("Paso 1: Creando usuarios de prueba...")
        user1_id = self.test_create_user("test_user_1", "test1@example.com", "pass123", "1990-01-01")
        self.wait_for_operation()
        
        user2_id = self.test_create_user("test_user_2", "test2@example.com", "pass456", "1992-02-02")
        self.wait_for_operation()
        
        user3_id = self.test_create_user("test_user_3", "test3@example.com", "pass789", "1995-03-03")
        self.wait_for_operation()
        
        if not all([user1_id, user2_id, user3_id]):
            self.print_error("No se pudieron crear usuarios de prueba. Abortando prueba.")
            if user1_id: self.test_delete_user(user1_id)
            if user2_id:self.test_delete_user(user2_id)
            if user3_id: self.test_delete_user(user3_id)
            return
        
        # Paso 2: Probar relaciones de amistad
        self.print_info("Paso 2: Probando relaciones de amistad...")
        self.test_add_friend(user1_id, user2_id)
        self.wait_for_operation()
        
        self.test_add_friend(user1_id, user3_id)
        self.wait_for_operation()
        
        self.test_add_friend(user2_id, user3_id)
        self.wait_for_operation()
        
        # Paso 3: Verificar amigos
        self.print_info("Paso 3: Verificando amigos...")
        self.test_get_user_friends(user1_id, expected_count=2)
        self.test_get_user_friends(user2_id, expected_count=2)
        self.test_get_user_friends(user3_id, expected_count=2)
        
        # Paso 4: Probar detalles de amigos
        self.print_info("Paso 4: Probando detalles de amigos...")
        self.test_get_friend_details(user1_id, user2_id)
        self.test_get_friend_details(user1_id, user3_id)
        
        # Paso 5: Probar eliminación de amigos
        self.print_info("Paso 5: Probando eliminación de amigos...")
        self.test_remove_friend(user1_id, user2_id)
        self.wait_for_operation()
        
        self.test_get_user_friends(user1_id, expected_count=1)
        
        # Paso 6: Probar actualización de usuarios
        self.print_info("Paso 6: Probando actualización de usuarios...")
        self.test_update_user(user1_id, "updated_user_1", "updated1@example.com", "1990-01-01")
        self.wait_for_operation()
        
        # Paso 7: Probar obtención de usuarios
        self.print_info("Paso 7: Probando obtención de usuarios...")
        self.test_get_user(user1_id)
        self.test_get_all_users()
        
        # Paso 8: Probar casos de error
        self.print_info("Paso 8: Probando casos de error...")
        self.test_get_user(9999, expected_success=False)  # Usuario inexistente
        self.test_add_friend(user1_id, 9999, expected_success=False)  # Amigo inexistente
        self.test_add_friend(user1_id, user1_id, expected_success=False)  # Auto-amistad
        
        # Paso 9: Limpieza
        self.print_info("Paso 9: Limpiando usuarios de prueba...")
        for user_id in self.created_users[:]:  # Copy list to avoid modification during iteration
            self.test_delete_user(user_id)
            self.wait_for_operation()
        
        # Resultados finales
        self.print_test_summary()
    
    def run_quick_test(self):
        """Ejecuta una prueba rápida con usuarios existentes"""
        self.print_header("INICIANDO PRUEBA RÁPIDA")
        
        # Usar usuarios existentes (ajusta estos IDs según tu base de datos)
        existing_users = [1, 2, 6]  # Cambia por IDs reales de tu BD
        
        for user_id in existing_users:
            self.test_get_user(user_id)
            self.wait_for_operation(0.5)
            
            self.test_get_user_friends(user_id)
            self.wait_for_operation(0.5)
        
        self.test_get_all_users()
        self.print_test_summary()
    
    def print_test_summary(self):
        """Imprime un resumen de los resultados de las pruebas"""
        self.print_header("RESUMEN DE PRUEBAS")
        print(f"✅ Pruebas exitosas: {self.test_results['passed']}")
        print(f"❌ Pruebas fallidas: {self.test_results['failed']}")
        print(f"📊 Total de pruebas: {self.test_results['passed'] + self.test_results['failed']}")
        
        if self.test_results['errors']:
            print(f"\n🔍 Errores encontrados:")
            for error in self.test_results['errors']:
                print(f"   - {error}")
        
        success_rate = (self.test_results['passed'] / (self.test_results['passed'] + self.test_results['failed'])) * 100
        print(f"\n🎯 Tasa de éxito: {success_rate:.1f}%")

# --- Ejemplos de uso ---
if __name__ == "__main__":
    tester = UsuarioTester()
    
    # Ejecutar prueba comprehensiva (crea y elimina usuarios de prueba)
    tester.run_comprehensive_test()
    
    # Ejecutar prueba rápida (usa usuarios existentes)
    # tester.run_quick_test()
    
    # O ejecutar pruebas individuales
    # tester.test_create_user("usuario_individual", "individual@test.com", "password123", "1995-05-05")
    # tester.test_get_all_users()
    # tester.test_add_friend(1, 2)  # Ajusta los IDs según tu BD
    # tester.test_get_user_friends(1)