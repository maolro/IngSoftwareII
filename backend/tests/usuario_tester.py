import requests
import json
import time
import random

# --- Configuración ---
BASE_URL = "http://localhost:8000/api"

class UsuarioTester:
    """Clase para realizar pruebas automatizadas de los endpoints de usuarios"""
    
    def __init__(self):
        self.created_ids = {
            'usuarios': []
        }
        self.test_results = {
            'passed': 0,
            'failed': 0,
            'errors': []
        }
        self.total_tests = 0
    
    def print_test_header(self, titulo):
        """Imprime un cabezal bonito para cada prueba"""
        print("\n" + "="*60)
        print(f" 👤 PRUEBA: {titulo}")
        print("="*60)
    
    def print_success(self, message):
        """Print success message"""
        print(f"✅ {message}")
        self.test_results['passed'] += 1
        self.total_tests += 1
    
    def print_error(self, message, error=None):
        """Print error message"""
        print(f"❌ {message}")
        if error:
            print(f"   Error: {error}")
        self.test_results['failed'] += 1
        self.total_tests += 1
        self.test_results['errors'].append(message)
    
    def print_info(self, message):
        """Print info message"""
        print(f"\nℹ️  {message}")
    
    def wait_for_operation(self, seconds=0.5):
        """Wait between operations to avoid race conditions"""
        time.sleep(seconds)

    def get_success_percentage(self):
        """Calculate and return success percentage"""
        if self.total_tests == 0:
            return 0.0
        return (self.test_results['passed'] / self.total_tests) * 100

    def print_progress(self):
        """Print current test progress"""
        success_pct = self.get_success_percentage()
        print(f"\n📊 Progreso: {self.test_results['passed']}/{self.total_tests} pruebas exitosas ({success_pct:.1f}%)")

    def cleanup(self):
        """Limpia todos los datos creados durante las pruebas"""
        self.print_test_header("LIMPIANDO DATOS DE PRUEBA")
        
        cleanup_count = 0
        
        # Limpiar usuarios
        for usuario_id in self.created_ids['usuarios'][:]:
            try:
                resp = requests.delete(f"{BASE_URL}/usuarios/{usuario_id}")
                if resp.status_code in [200, 204]:
                    print(f"✅ Usuario eliminado: {usuario_id}")
                    self.created_ids['usuarios'].remove(usuario_id)
                    cleanup_count += 1
                else:
                    print(f"⚠️  No se pudo eliminar usuario {usuario_id}: {resp.status_code}")
            except Exception as e:
                print(f"❌ Error eliminando usuario {usuario_id}: {e}")
        
        print(f"🧹 Limpieza completada: {cleanup_count} elementos eliminados")

    def test_crear_usuario(self, username, email, password, birth_date, expected_success=True):
        """Prueba para crear usuario"""
        usuario_data = {
            "username": username,
            "email": email,
            "password": password,
            "birth_date": birth_date
        }
        
        try:
            resp = requests.post(f"{BASE_URL}/usuarios/", json=usuario_data)
            
            if expected_success and resp.status_code == 201:
                usuario_id = resp.json()['id']
                self.created_ids['usuarios'].append(usuario_id)
                self.print_success(f"Usuario creado: {username} (ID: {usuario_id})")
                return usuario_id
            elif not expected_success and resp.status_code != 201:
                self.print_success(f"Creación fallida como se esperaba: {resp.status_code}")
                return None
            else:
                self.print_error(f"Resultado inesperado. {resp.status_code} - {resp.json()['error']}")
                return None
                
        except Exception as e:
            self.print_error(f"Error creando usuario: {e}")
            return None

    def test_obtener_usuario_por_id(self, usuario_id, expected_success=True):
        """Prueba obtener usuario por ID"""
        self.print_test_header(f"OBTENER USUARIO POR ID: {usuario_id}")
        
        try:
            resp = requests.get(f"{BASE_URL}/usuarios/{usuario_id}/")
            
            if expected_success and resp.status_code == 200:
                detalle = resp.json()
                self.print_success(f"Usuario obtenido: {detalle['username']}")
                return detalle
            elif not expected_success and resp.status_code == 404:
                self.print_success("Usuario no encontrado (como se esperaba)")
                return None
            else:
                self.print_error(f"Resultado inesperado. {resp.status_code} - {resp.json()['error']}")
                return None
                
        except Exception as e:
            self.print_error(f"Error obteniendo usuario: {e}")
            return None

    def test_obtener_todos_usuarios(self, expected_min_count=0):
        """Prueba obtener todos los usuarios"""
        self.print_test_header("OBTENER TODOS LOS USUARIOS")
        
        try:
            resp = requests.get(f"{BASE_URL}/usuarios/")
            
            if resp.status_code == 200:
                usuarios = resp.json()
                if len(usuarios) >= expected_min_count:
                    self.print_success(f"Obtenidos {len(usuarios)} usuarios")
                    return usuarios
                else:
                    self.print_error(f"Se esperaban al menos {expected_min_count} usuarios, se obtuvieron {len(usuarios)}")
                    return usuarios
            else:
                self.print_error(f"Error obteniendo usuarios. Código: {resp.status_code}")
                return None
                
        except Exception as e:
            self.print_error(f"Error obteniendo usuarios: {e}")
            return None

    def test_actualizar_usuario(self, usuario_id, nuevos_datos, expected_success=True):
        """Prueba actualizar usuario"""
        self.print_test_header(f"ACTUALIZAR USUARIO: {usuario_id}")
        
        try:
            resp = requests.put(f"{BASE_URL}/usuarios/{usuario_id}/", json=nuevos_datos)
            
            if expected_success and resp.status_code == 200:
                usuario_actualizado = resp.json()
                self.print_success(f"Usuario actualizado: {resp.json()['username']}")
                return usuario_actualizado
            elif not expected_success and resp.status_code != 200:
                self.print_success("Actualización fallida como se esperaba")
                return None
            else:
                self.print_error(f"Resultado inesperado. {resp.status_code} - {resp.json()['error']}")
                return None
                
        except Exception as e:
            self.print_error(f"Error actualizando usuario: {e}")
            return None

    def test_eliminar_usuario(self, usuario_id, expected_success=True):
        """Prueba eliminar usuario"""
        self.print_test_header(f"ELIMINAR USUARIO: {usuario_id}")
        
        try:
            resp = requests.delete(f"{BASE_URL}/usuarios/{usuario_id}")
            
            if expected_success and resp.status_code == 200:
                self.print_success(f"Usuario {usuario_id} eliminado exitosamente")
                if usuario_id in self.created_ids['usuarios']:
                    self.created_ids['usuarios'].remove(usuario_id)
                return True
            elif not expected_success and resp.status_code == 404:
                self.print_success("Eliminación fallida como se esperaba (usuario no existe)")
                return False
            else:
                self.print_error(f"Resultado inesperado. {resp.status_code} - {resp.json()['error']}")
                return False
                
        except Exception as e:
            self.print_error(f"Error eliminando usuario: {e}")
            return False

    def test_agregar_amigo(self, usuario_id, amigo_id, expected_success=True):
        """Prueba agregar amigo a usuario"""
        self.print_test_header(f"AGREGAR AMIGO: Usuario {usuario_id} -> Amigo {amigo_id}")
        
        amigo_data = {
            "friend_id": amigo_id
        }
        
        try:
            resp = requests.post(f"{BASE_URL}/usuarios/{usuario_id}/amigos/", json=amigo_data)
            
            if expected_success and resp.status_code == 201:
                resultado = resp.json()
                if resultado.get('success'):
                    self.print_success(f"Amigo agregado: {usuario_id} -> {amigo_id}")
                    return True
                else:
                    self.print_error(f"Amigo no agregado: {resultado.get('error', 'Error desconocido')}")
                    return False
            elif not expected_success and resp.status_code != 201:
                self.print_success("Agregar amigo falló como se esperaba")
                return False
            else:
                self.print_error(f"Resultado inesperado. {resp.status_code} - {resp.json()['error']}")
                return False
                
        except Exception as e:
            self.print_error(f"Error agregando amigo: {e}")
            return False

    def test_obtener_amigos_usuario(self, usuario_id, expected_min_count=0):
        """Prueba obtener amigos de usuario"""
        self.print_test_header(f"OBTENER AMIGOS DE USUARIO: {usuario_id}")
        
        try:
            resp = requests.get(f"{BASE_URL}/usuarios/{usuario_id}/amigos/")
            
            if resp.status_code == 200:
                amigos = resp.json()
                if len(amigos) >= expected_min_count:
                    self.print_success(f"Obtenidos {len(amigos)} amigos del usuario")
                    return amigos
                else:
                    self.print_error(f"Se esperaban al menos {expected_min_count} amigos, se obtuvieron {len(amigos)}")
                    return amigos
            else:
                self.print_error(f"Error obteniendo amigos. {resp.status_code} - {resp.json()['error']}")
                return None
                
        except Exception as e:
            self.print_error(f"Error obteniendo amigos: {e}")
            return None

    def test_obtener_detalles_amigo(self, usuario_id, amigo_id, expected_success=True):
        """Prueba obtener detalles de amigo específico"""
        self.print_test_header(f"OBTENER DETALLES DE AMIGO: Usuario {usuario_id} -> Amigo {amigo_id}")
        
        try:
            resp = requests.get(f"{BASE_URL}/usuarios/{usuario_id}/amigos/{amigo_id}/")
            
            if expected_success and resp.status_code == 200:
                detalle_amigo = resp.json()
                self.print_success(f"Detalles de amigo obtenidos: {detalle_amigo['username']}")
                return detalle_amigo
            elif not expected_success and resp.status_code == 404:
                self.print_success("Amigo no encontrado (como se esperaba)")
                return None
            else:
                self.print_error(f"Resultado inesperado. {resp.status_code} - {resp.json()['error']}")
                return None
                
        except Exception as e:
            self.print_error(f"Error obteniendo detalles de amigo: {e}")
            return None

    def test_eliminar_amigo(self, usuario_id, amigo_id, expected_success=True):
        """Prueba eliminar amigo de usuario"""
        self.print_test_header(f"ELIMINAR AMIGO: Usuario {usuario_id} -> Amigo {amigo_id}")
        
        try:
            resp = requests.delete(f"{BASE_URL}/usuarios/{usuario_id}/amigos/{amigo_id}/")
            
            if expected_success and resp.status_code == 200:
                resultado = resp.json()
                if resultado.get('success'):
                    self.print_success(f"Amigo eliminado: {usuario_id} -> {amigo_id}")
                    return True
                else:
                    self.print_error(f"Amigo no eliminado: {resultado.get('error', 'Error desconocido')}")
                    return False
            elif not expected_success and resp.status_code != 200:
                self.print_success("Eliminar amigo falló como se esperaba")
                return False
            else:
                self.print_error(f"Resultado inesperado. {resp.status_code} - {resp.json()['error']}")
                return False
                
        except Exception as e:
            self.print_error(f"Error eliminando amigo: {e}")
            return False

    def test_servidor_conectado(self):
        """Prueba conexión al servidor"""
        self.print_test_header("CONEXIÓN AL SERVIDOR")
        
        try:
            home_resp = requests.get("http://localhost:8000/")
            home_resp.raise_for_status()
            self.print_success(f"Servidor conectado: {home_resp.json()['message']}")
            return True
        except requests.exceptions.ConnectionError:
            self.print_error("No se pudo conectar al servidor")
            return False
        except Exception as e:
            self.print_error(f"Error inesperado: {e}")
            return False

    def test_crear_usuario_duplicado(self, usuario_data):
        """Prueba crear usuario duplicado"""
        self.print_test_header("CREAR USUARIO DUPLICADO")
        
        try:
            resp = requests.post(f"{BASE_URL}/usuarios/", json=usuario_data)
            
            if resp.status_code == 409:
                self.print_success("Error 409 recibido correctamente (conflicto de duplicados)")
                return True
            else:
                self.print_error(f"Se esperaba 409 pero se recibió {resp.status_code}")
                return False
                
        except Exception as e:
            self.print_error(f"Error creando usuario duplicado: {e}")
            return False

    def test_agregar_amigo_a_si_mismo(self, usuario_id):
        """Prueba agregarse a sí mismo como amigo"""
        self.print_test_header(f"AGREGARSE A SÍ MISMO COMO AMIGO: {usuario_id}")
        
        amigo_data = {
            "friend_id": usuario_id
        }
        
        try:
            resp = requests.post(f"{BASE_URL}/usuarios/{usuario_id}/amigos/", json=amigo_data)
            
            if resp.status_code == 400:
                self.print_success("Error 400 recibido correctamente (no se puede agregar a sí mismo)")
                return True
            else:
                self.print_error(f"Se esperaba 400 pero se recibió {resp.status_code}")
                return False
                
        except Exception as e:
            self.print_error(f"Error probando auto-amistad: {e}")
            return False

    def run_comprehensive_test(self):
        """Ejecuta una prueba completa de todos los endpoints de usuarios"""
        self.print_test_header("INICIANDO PRUEBA COMPREHENSIVA DE USUARIOS")
        
        # Paso 0: Verificar servidor
        self.print_info("Paso 0: Verificando conexión al servidor...")
        if not self.test_servidor_conectado():
            return
        
        # Paso 1: Crear usuarios de prueba
        self.print_info("Paso 1: Creando usuarios de prueba...")
        
        usuario1_id = self.test_crear_usuario(
            "usuario_prueba_1", 
            "prueba1@test.com",
            "password123",
            "1990-01-01"
        )
        self.wait_for_operation()
        
        usuario2_id = self.test_crear_usuario(
            "usuario_prueba_2",
            "prueba2@test.com", 
            "password456",
            "1992-02-02"
        )
        self.wait_for_operation()
        
        usuario3_id = self.test_crear_usuario(
            "usuario_prueba_3",
            "prueba3@test.com",
            "password789", 
            "1995-03-03"
        )
        self.wait_for_operation()
        
        if not all([usuario1_id, usuario2_id, usuario3_id]):
            self.print_error("No se pudieron crear usuarios de prueba. Abortando prueba.")
            self.cleanup()
            return
        
        # Paso 2: Probar obtención de usuarios
        self.print_info("Paso 2: Probando obtención de usuarios...")
        self.test_obtener_usuario_por_id(usuario1_id)
        self.wait_for_operation()
        
        self.test_obtener_todos_usuarios(expected_min_count=3)
        self.wait_for_operation()
        
        # Paso 3: Probar actualización de usuarios
        self.print_info("Paso 3: Probando actualización de usuarios...")
        self.test_actualizar_usuario(
            usuario1_id,
            {
                "username": "usuario_actualizado_1",
                "email": "actualizado1@test.com",
                "birth_date": "1990-01-01"
            }
        )
        self.wait_for_operation()
        
        # Paso 4: Probar relaciones de amistad
        self.print_info("Paso 4: Probando relaciones de amistad...")
        self.test_agregar_amigo(usuario1_id, usuario2_id)
        self.wait_for_operation()
        
        self.test_agregar_amigo(usuario1_id, usuario3_id)
        self.wait_for_operation()
        
        self.test_agregar_amigo(usuario2_id, usuario3_id)
        self.wait_for_operation()
        
        # Paso 5: Verificar amigos
        self.print_info("Paso 5: Verificando amigos...")
        self.test_obtener_amigos_usuario(usuario1_id, expected_min_count=2)
        self.wait_for_operation()
        
        self.test_obtener_detalles_amigo(usuario1_id, usuario2_id)
        self.wait_for_operation()
        
        # Paso 6: Probar eliminación de amigos
        self.print_info("Paso 6: Probando eliminación de amigos...")
        self.test_eliminar_amigo(usuario1_id, usuario2_id)
        self.wait_for_operation()
        
        self.test_obtener_amigos_usuario(usuario1_id, expected_min_count=1)
        self.wait_for_operation()
        
        # Paso 7: Probar casos de error
        self.print_info("Paso 7: Probando casos de error...")
        self.test_obtener_usuario_por_id(9999, expected_success=False)
        self.wait_for_operation()
        
        # Probar crear usuario duplicado
        usuario_data_duplicado = {
            "username": "usuario_actualizado_1",
            "email": "duplicado@test.com",
            "password": "password123",
            "birth_date": "1990-01-01"
        }
        self.test_crear_usuario_duplicado(usuario_data_duplicado)
        self.wait_for_operation()
        
        # Probar agregarse a sí mismo como amigo
        self.test_agregar_amigo_a_si_mismo(usuario1_id)
        self.wait_for_operation()
        
        # Paso 8: Probar eliminación
        self.print_info("Paso 8: Probando eliminación de usuarios...")
        # Eliminar solo uno para demostrar la funcionalidad
        if self.created_ids['usuarios']:
            usuario_a_eliminar = self.created_ids['usuarios'][0]
            self.test_eliminar_usuario(usuario_a_eliminar)
            self.wait_for_operation()
        
        # Resultados finales
        self.print_test_summary()

    def run_quick_test(self):
        """Ejecuta una prueba rápida con datos existentes"""
        self.print_test_header("INICIANDO PRUEBA RÁPIDA DE USUARIOS")
        
        # Verificar servidor
        if not self.test_servidor_conectado():
            return
        
        # Probar endpoints básicos con datos existentes
        self.test_obtener_todos_usuarios()
        self.wait_for_operation()
        
        # Si hay usuarios, probar obtener uno específico
        usuarios = self.test_obtener_todos_usuarios()
        if usuarios and len(usuarios) > 0:
            primer_usuario_id = usuarios[0]['user_id']
            self.test_obtener_usuario_por_id(primer_usuario_id)
            self.wait_for_operation()
            
            # Probar obtener amigos si el usuario existe
            self.test_obtener_amigos_usuario(primer_usuario_id)
            self.wait_for_operation()
        
        self.print_test_summary()

    def print_test_summary(self):
        """Imprime un resumen de los resultados de las pruebas"""
        self.print_test_header("RESUMEN DE PRUEBAS DE USUARIOS")
        print(f"✅ Pruebas exitosas: {self.test_results['passed']}")
        print(f"❌ Pruebas fallidas: {self.test_results['failed']}")
        print(f"📊 Total de pruebas: {self.total_tests}")
        
        if self.test_results['errors']:
            print(f"\n🔍 Errores encontrados:")
            for error in self.test_results['errors']:
                print(f"   - {error}")
        
        success_pct = self.get_success_percentage()
        print(f"\n🎯 Tasa de éxito: {success_pct:.1f}%")
        
        if self.test_results['failed'] == 0 and self.test_results['passed'] > 0:
            print("\n🎉 ¡TODAS LAS PRUEBAS DE USUARIOS EXITOSAS!")
        elif self.test_results['passed'] > 0:
            print("\n⚠️  Algunas pruebas fallaron, pero otras fueron exitosas")
        else:
            print("\n💥 Todas las pruebas fallaron")

# --- Ejecución de pruebas ---
if __name__ == "__main__":
    tester = UsuarioTester()
    
    print("Iniciando pruebas de API de Usuarios...")
    print("Asegúrate de que el servidor Flask esté ejecutándose en http://localhost:8000")
    time.sleep(2)
    
    # Ejecutar prueba comprehensiva (crea y elimina datos de prueba)
    tester.run_comprehensive_test()
    
    # O ejecutar prueba rápida (usa datos existentes)
    # tester.run_quick_test()
    
    # Limpieza final
    tester.cleanup()