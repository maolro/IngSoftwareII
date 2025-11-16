import requests
import json
import time
import random

# --- Configuración ---
BASE_URL = "http://localhost:8000/api"

class CerveceriaTester:
    """Clase para realizar pruebas automatizadas de los endpoints de cervecerías"""
    
    def __init__(self):
        self.created_ids = {
            'cervecerias': [],
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
        print(f" PRUEBA: {titulo}")
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
        
        # Limpiar cervecerías
        for cerveceria_id in self.created_ids['cervecerias'][:]:
            try:
                # Nota: Asumiendo que hay un endpoint DELETE para cervecerías
                # Si no existe, puedes omitir esta parte
                resp = requests.delete(f"{BASE_URL}/cervecerias/{cerveceria_id}")
                if resp.status_code in [200, 204]:
                    print(f"✅ Cervecería eliminada: {cerveceria_id}")
                    self.created_ids['cervecerias'].remove(cerveceria_id)
                    cleanup_count += 1
                else:
                    print(f"⚠️  No se pudo eliminar cervecería {cerveceria_id}: {resp.status_code}")
            except Exception as e:
                print(f"❌ Error eliminando cervecería {cerveceria_id}: {e}")
        
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

    def crear_usuario_prueba(self, username_suffix=""):
        """Crea un usuario de prueba para los 'me gusta'"""
        username = f"cerveceria_test_user{username_suffix}"
        usuario_data = {
            "username": username,
            "email": f"cerveceria_test{username_suffix}@test.com",
            "birth_date": "1990-01-01",
            "password": "test_password_123"
        }
        
        try:
            resp = requests.post(f"{BASE_URL}/usuarios/", json=usuario_data)
            if resp.status_code == 201:
                usuario_id = resp.json()['id']
                self.created_ids['usuarios'].append(usuario_id)
                self.print_success(f"Usuario de prueba creado: {usuario_id}")
                return usuario_id
            else:
                error_msg = resp.json().get('error', 'Error desconocido')
                self.print_error(f"Resultado inesperado. {resp.status_code} - {error_msg}")
                return None
        except Exception as e:
            self.print_error(f"Error creando usuario: {e}")
            return None

    def test_crear_cerveceria(self, nombre, direccion, ciudad=None, pais=None, expected_success=True):
        """Prueba para crear cervecería"""
        cerveceria_data = {
            "nombre": nombre,
            "direccion": direccion,
            "ciudad": ciudad,
            "pais": pais,
            "descripcion": f"Descripción de prueba para {nombre}",
            "telefono": f"+34 {random.randint(600000000, 699999999)}",
            "horario": "L-V: 18:00-02:00, S-D: 12:00-03:00",
            "foto": f"foto_{nombre.lower().replace(' ', '_')}.jpg"
        }
        
        try:
            resp = requests.post(f"{BASE_URL}/cervecerias/", json=cerveceria_data)
            
            if expected_success and resp.status_code == 201:
                cerveceria_id = resp.json()['id']
                self.created_ids['cervecerias'].append(cerveceria_id)
                self.print_success(f"Cervecería creada: {nombre} (ID: {cerveceria_id})")
                return cerveceria_id
            elif not expected_success and resp.status_code != 201:
                self.print_success(f"Creación fallida como se esperaba: {resp.status_code}")
                return None
            else:
                error_msg = resp.json().get('error', 'Error desconocido')
                self.print_error(f"Resultado inesperado. {resp.status_code} - {error_msg}")
                return None
                
        except Exception as e:
            self.print_error(f"Error creando cervecería: {e}")
            return None

    def test_obtener_cerveceria_por_id(self, cerveceria_id, expected_success=True):
        """Prueba obtener cervecería por ID"""
        self.print_test_header(f"OBTENER CERVECERÍA POR ID: {cerveceria_id}")
        
        try:
            resp = requests.get(f"{BASE_URL}/cervecerias/{cerveceria_id}/")
            
            if expected_success and resp.status_code == 200:
                detalle = resp.json()
                self.print_success(f"Cervecería obtenida: {detalle['nombre']}")
                return detalle
            elif not expected_success and resp.status_code == 404:
                self.print_success("Cervecería no encontrada (como se esperaba)")
                return None
            else:
                self.print_error(f"Resultado inesperado. {resp.status_code} - {resp.text}")
                return None
                
        except Exception as e:
            self.print_error(f"Error obteniendo cervecería: {e}")
            return None

    def test_buscar_cervecerias(self, q=None, ciudad=None, pais=None, expected_min_count=0):
        """Prueba buscar cervecerías con filtros"""
        self.print_test_header("BUSCAR CERVECERÍAS")
        
        try:
            params = {}
            if q:
                params['q'] = q
            if ciudad:
                params['ciudad'] = ciudad
            if pais:
                params['pais'] = pais
                
            resp = requests.get(f"{BASE_URL}/cervecerias/", params=params)
            
            if resp.status_code == 200:
                cervecerias = resp.json()
                if len(cervecerias) >= expected_min_count:
                    self.print_success(f"Obtenidas {len(cervecerias)} cervecerías")
                    if q or ciudad or pais:
                        filtros = []
                        if q: filtros.append(f"q={q}")
                        if ciudad: filtros.append(f"ciudad={ciudad}")
                        if pais: filtros.append(f"pais={pais}")
                        self.print_info(f"Filtros aplicados: {', '.join(filtros)}")
                    return cervecerias
                else:
                    self.print_error(f"Se esperaban al menos {expected_min_count} cervecerías, se obtuvieron {len(cervecerias)}")
                    return cervecerias
            else:
                self.print_error(f"Error buscando cervecerías. Código: {resp.status_code}")
                return None
                
        except Exception as e:
            self.print_error(f"Error buscando cervecerías: {e}")
            return None

    def test_obtener_cervecerias_sugeridas(self, lat, lon, radio=5, expected_min_count=0):
        """Prueba obtener cervecerías sugeridas por geolocalización"""
        self.print_test_header(f"OBTENER CERVECERÍAS SUGERIDAS (lat={lat}, lon={lon}, radio={radio}km)")
        
        try:
            params = {
                'lat': lat,
                'lon': lon,
                'radio': radio
            }
                
            resp = requests.get(f"{BASE_URL}/cervecerias/sugeridas/", params=params)
            
            if resp.status_code == 200:
                sugerencias = resp.json()
                if len(sugerencias) >= expected_min_count:
                    self.print_success(f"Obtenidas {len(sugerencias)} cervecerías sugeridas")
                    return sugerencias
                else:
                    self.print_error(f"Se esperaban al menos {expected_min_count} sugerencias, se obtuvieron {len(sugerencias)}")
                    return sugerencias
            else:
                self.print_error(f"Error obteniendo sugerencias. Código: {resp.status_code}")
                return None
                
        except Exception as e:
            self.print_error(f"Error obteniendo sugerencias: {e}")
            return None

    def test_marcar_me_gusta(self, cerveceria_id, usuario_id, expected_success=True):
        """Prueba marcar 'me gusta' en cervecería"""
        self.print_test_header(f"MARCAR 'ME GUSTA': Cervecería {cerveceria_id} - Usuario {usuario_id}")
        
        me_gusta_data = {
            "usuario_id": usuario_id
        }
        
        try:
            resp = requests.post(f"{BASE_URL}/cervecerias/{cerveceria_id}/me-gusta/", json=me_gusta_data)
            
            if expected_success and resp.status_code == 201:
                resultado = resp.json()
                self.print_success(f"'Me gusta' marcado: {resultado.get('mensaje', 'Éxito')}")
                return resultado
            elif not expected_success and resp.status_code != 201:
                self.print_success("Marcar 'me gusta' falló como se esperaba")
                return None
            else:
                error_msg = resp.json().get('error', 'Error desconocido')
                self.print_error(f"Resultado inesperado. {resp.status_code} - {error_msg}")
                return None
                
        except Exception as e:
            self.print_error(f"Error marcando 'me gusta': {e}")
            return None

    def test_crear_cerveceria_duplicada(self, cerveceria_data):
        """Prueba crear cervecería duplicada"""
        self.print_test_header("CREAR CERVECERÍA DUPLICADA")
        
        try:
            resp = requests.post(f"{BASE_URL}/cervecerias/", json=cerveceria_data)
            
            if resp.status_code == 409:
                self.print_success("Error 409 recibido correctamente (conflicto de duplicados)")
                return True
            else:
                self.print_error(f"Se esperaba 409 pero se recibió {resp.status_code}")
                return False
                
        except Exception as e:
            self.print_error(f"Error creando cervecería duplicada: {e}")
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

    def test_cerveceria_sin_campos_obligatorios(self):
        """Prueba crear cervecería sin campos obligatorios"""
        self.print_test_header("CREAR CERVECERÍA SIN CAMPOS OBLIGATORIOS")
        
        cerveceria_data_incompleta = {
            "ciudad": "Madrid",
            "descripcion": "Falta nombre y dirección"
        }
        
        try:
            resp = requests.post(f"{BASE_URL}/cervecerias/", json=cerveceria_data_incompleta)
            
            if resp.status_code == 400:
                self.print_success("Error 400 recibido correctamente (campos obligatorios faltantes)")
                return True
            else:
                self.print_error(f"Se esperaba 400 pero se recibió {resp.status_code}")
                return False
                
        except Exception as e:
            self.print_error(f"Error probando campos obligatorios: {e}")
            return False

    def test_me_gusta_sin_usuario_id(self, cerveceria_id):
        """Prueba marcar 'me gusta' sin usuario_id"""
        self.print_test_header("MARCAR 'ME GUSTA' SIN USUARIO_ID")
        
        me_gusta_data_incompleto = {
            "campo_incorrecto": 123
        }
        
        try:
            resp = requests.post(f"{BASE_URL}/cervecerias/{cerveceria_id}/me-gusta/", json=me_gusta_data_incompleto)
            
            if resp.status_code == 400:
                self.print_success("Error 400 recibido correctamente (usuario_id faltante)")
                return True
            else:
                self.print_error(f"Se esperaba 400 pero se recibió {resp.status_code}")
                return False
                
        except Exception as e:
            self.print_error(f"Error probando 'me gusta' sin usuario_id: {e}")
            return False

    def run_comprehensive_test(self):
        """Ejecuta una prueba completa de todos los endpoints de cervecerías"""
        self.print_test_header("INICIANDO PRUEBA COMPREHENSIVA DE CERVECERÍAS")
        
        # Paso 0: Verificar servidor
        self.print_info("Paso 0: Verificando conexión al servidor...")
        if not self.test_servidor_conectado():
            return
        
        # Paso 1: Crear cervecerías de prueba
        self.print_info("Paso 1: Creando cervecerías de prueba...")
        
        cerveceria1_id = self.test_crear_cerveceria(
            "Cervecería La Tradición", 
            "Calle Mayor 123",
            "Madrid",
            "España"
        )
        self.wait_for_operation()
        
        cerveceria2_id = self.test_crear_cerveceria(
            "Brew & Blues",
            "Avenida Libertad 45",
            "Barcelona", 
            "España"
        )
        self.wait_for_operation()
        
        cerveceria3_id = self.test_crear_cerveceria(
            "Hoppy Corner",
            "Plaza Central 67",
            "Valencia",
            "España"
        )
        self.wait_for_operation()
        
        cerveceria4_id = self.test_crear_cerveceria(
            "Munich Haus",
            "Beer Street 89",
            "Berlín",
            "Alemania"
        )
        self.wait_for_operation()
        
        if not all([cerveceria1_id, cerveceria2_id, cerveceria3_id]):
            self.print_error("No se pudieron crear cervecerías de prueba. Abortando prueba.")
            self.cleanup()
            return
        
        # Paso 2: Probar obtención de cervecerías
        self.print_info("Paso 2: Probando obtención de cervecerías...")
        self.test_obtener_cerveceria_por_id(cerveceria1_id)
        self.wait_for_operation()
        
        self.test_buscar_cervecerias(expected_min_count=4)
        self.wait_for_operation()
        
        # Paso 3: Probar búsquedas con filtros
        self.print_info("Paso 3: Probando búsquedas con filtros...")
        self.test_buscar_cervecerias(q="Tradición", expected_min_count=1)
        self.wait_for_operation()
        
        self.test_buscar_cervecerias(ciudad="Madrid", expected_min_count=1)
        self.wait_for_operation()
        
        self.test_buscar_cervecerias(pais="Alemania", expected_min_count=1)
        self.wait_for_operation()
        
        # Paso 4: Probar casos de error
        self.print_info("Paso 5: Probando casos de error...")
        self.test_obtener_cerveceria_por_id(9999, expected_success=False)
        self.wait_for_operation()
        
        # Probar crear cervecería duplicada
        cerveceria_data_duplicada = {
            "nombre": "Cervecería La Tradición",  # Mismo nombre que la primera
            "direccion": "Otra dirección diferente",
            "ciudad": "Madrid",
            "pais": "España"
        }
        self.test_crear_cerveceria_duplicada(cerveceria_data_duplicada)
        self.wait_for_operation()
        
        # Probar crear cervecería sin campos obligatorios
        self.test_cerveceria_sin_campos_obligatorios()
        self.wait_for_operation()
        
        # Paso 5: Probar búsqueda avanzada
        self.print_info("Paso 6: Probando búsqueda avanzada...")
        self.test_buscar_cervecerias(q="Brew", ciudad="Barcelona", expected_min_count=1)
        self.wait_for_operation()
        
        # Resultados finales
        self.print_test_summary()

    def run_quick_test(self):
        """Ejecuta una prueba rápida con datos existentes"""
        self.print_test_header("INICIANDO PRUEBA RÁPIDA DE CERVECERÍAS")
        
        # Verificar servidor
        if not self.test_servidor_conectado():
            return
        
        # Probar endpoints básicos con datos existentes
        self.test_buscar_cervecerias()
        self.wait_for_operation()
        
        # Si hay cervecerías, probar obtener una específica
        cervecerias = self.test_buscar_cervecerias()
        if cervecerias and len(cervecerias) > 0:
            primera_cerveceria_id = cervecerias[0]['id']
            self.test_obtener_cerveceria_por_id(primera_cerveceria_id)
            self.wait_for_operation()
            
            # Probar sugerencias si hay coordenadas
            self.test_obtener_cervecerias_sugeridas(40.4168, -3.7038, radio=5)
            self.wait_for_operation()
        
        self.print_test_summary()

    def print_test_summary(self):
        """Imprime un resumen de los resultados de las pruebas"""
        self.print_test_header("RESUMEN DE PRUEBAS DE CERVECERÍAS")
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
            print("\n🎉 ¡TODAS LAS PRUEBAS DE CERVECERÍAS EXITOSAS!")
        elif self.test_results['passed'] > 0:
            print("\n⚠️  Algunas pruebas fallaron, pero otras fueron exitosas")
        else:
            print("\n💥 Todas las pruebas fallaron")

# --- Ejecución de pruebas ---
if __name__ == "__main__":
    tester = CerveceriaTester()
    
    print("Iniciando pruebas de API de Cervecerías...")
    print("Asegúrate de que el servidor Flask esté ejecutándose en http://localhost:8000")
    time.sleep(2)
    
    # Ejecutar prueba comprehensiva (crea y elimina datos de prueba)
    tester.run_comprehensive_test()
    
    # O ejecutar prueba rápida (usa datos existentes)
    # tester.run_quick_test()
    
    # Limpieza final
    tester.cleanup()