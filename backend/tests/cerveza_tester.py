import requests
import json
import time
import random

# --- Configuración ---
BASE_URL = "http://localhost:8000/api"

class CervezaTester:
    """Clase para realizar pruebas automatizadas de los endpoints de cervezas"""
    
    def __init__(self):
        self.created_ids = {
            'cervezas': [],
            'usuarios': [],
            'cervecerias': [],
            'degustaciones': []
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
        print(f"\nℹ️  {message} \n")
    
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
        
        # Limpiar degustaciones primero (dependencias)
        for degustacion_id in self.created_ids['degustaciones'][:]:
            try:
                resp = requests.delete(f"{BASE_URL}/degustaciones/{degustacion_id}/")
                if resp.status_code in [200, 204]:
                    print(f"✅ Degustación eliminada: {degustacion_id}")
                    self.created_ids['degustaciones'].remove(degustacion_id)
                    cleanup_count += 1
                else:
                    print(f"⚠️  No se pudo eliminar degustación {degustacion_id}: {resp.status_code}")
            except Exception as e:
                print(f"❌ Error eliminando degustación {degustacion_id}: {e}")
        
        # Limpiar cervezas
        for cerveza_id in self.created_ids['cervezas'][:]:
            try:
                resp = requests.delete(f"{BASE_URL}/cervezas/{cerveza_id}/")
                if resp.status_code in [200, 204]:
                    print(f"✅ Cerveza eliminada: {cerveza_id}")
                    self.created_ids['cervezas'].remove(cerveza_id)
                    cleanup_count += 1
                else:
                    print(f"⚠️  No se pudo eliminar cerveza {cerveza_id}: {resp.status_code}")
            except Exception as e:
                print(f"❌ Error eliminando cerveza {cerveza_id}: {e}")
        
        # Limpiar usuarios
        for usuario_id in self.created_ids['usuarios'][:]:
            try:
                resp = requests.delete(f"{BASE_URL}/usuarios/{usuario_id}/")
                if resp.status_code in [200, 204]:
                    print(f"✅ Usuario eliminado: {usuario_id}")
                    self.created_ids['usuarios'].remove(usuario_id)
                    cleanup_count += 1
                else:
                    print(f"⚠️  No se pudo eliminar usuario {usuario_id}: {resp.status_code}")
            except Exception as e:
                print(f"❌ Error eliminando usuario {usuario_id}: {e}")

        for cerveceria_id in self.created_ids['cervecerias'][:]:
            try:
                resp = requests.delete(f"{BASE_URL}/cervecerias/{cerveceria_id}/")
                if resp.status_code in [200, 204]:
                    print(f"✅ Cervecería eliminada: {cerveceria_id}")
                    self.created_ids['cervecerias'].remove(cerveceria_id)
                    cleanup_count += 1
                else:
                    print(f"⚠️  No se pudo eliminar cerveceria {cerveceria_id}: {resp.status_code}")
            except Exception as e:
                print(f"❌ Error eliminando cerveceria {cerveceria_id}: {e}")
        
        print(f"🧹 Limpieza completada: {cleanup_count} elementos eliminados")

    def crear_usuario_prueba(self, username=""):
        """Crea un usuario de prueba para las degustaciones"""
        if not username:
            username = f"usuario_test_{random.randint(1000, 9999)}"
            
        usuario_data = {
            "username": username,
            "email": f"{username}@test.com",
            "birth_date": "1990-01-01",
            "password": "test_password_123"
        }
        
        try:
            resp = requests.post(f"{BASE_URL}/usuarios/", json=usuario_data)
            if resp.status_code == 201:
                usuario_id = resp.json()['id']
                self.created_ids['usuarios'].append(usuario_id)
                self.print_success(f"Usuario de prueba creado: {username} (ID: {usuario_id})")
                return usuario_id
            else:
                error_msg = resp.json().get('error', 'Error desconocido')
                self.print_error(f"Error creando usuario: {resp.status_code} - {error_msg}")
                return None
        except Exception as e:
            self.print_error(f"Error creando usuario: {e}")
            return None

    def test_crear_degustacion(self, usuario_id, cerveza_id, cerveceria_id, puntuacion,
    expected_success=True):
        """Prueba para crear degustación"""
        degustacion_data = {
            "usuario_id": usuario_id,
            "cerveza_id": cerveza_id,
            "cerveceria_id": cerveceria_id,
            "puntuacion": puntuacion,
            "comentario": f"Esta es una degustación de prueba creada el {time.strftime('%Y-%m-%d %H:%M:%S')}"
        }
        
        if cerveceria_id:
            degustacion_data["cerveceria_id"] = cerveceria_id
        
        try:
            resp = requests.post(f"{BASE_URL}/degustaciones/", json=degustacion_data)
            
            if expected_success and resp.status_code == 201:
                degustacion_id = resp.json()['id']
                self.created_ids['degustaciones'].append(degustacion_id)
                self.print_success(f"Degustación creada: ID {degustacion_id} (Puntuación: {degustacion_data['puntuacion']})")
                return degustacion_id
            elif not expected_success and resp.status_code != 201:
                self.print_success(f"Creación fallida como se esperaba: {resp.status_code}")
                return None
            else:
                error_msg = resp.json().get('error', 'Error desconocido')
                self.print_error(f"Resultado inesperado. {resp.status_code} - {error_msg}")
                return None
                
        except Exception as e:
            self.print_error(f"Error creando degustación: {e}")
            return None

    def test_crear_cerveza(self, cerveza_data, expected_success=True):
        """Prueba para crear cerveza - RF-3.2"""
        self.print_test_header(f"CREAR CERVEZA: {cerveza_data.get('nombre', 'Sin nombre')}")
        
        try:
            resp = requests.post(f"{BASE_URL}/cervezas/", json=cerveza_data)
            
            if expected_success and resp.status_code == 201:
                cerveza_id = resp.json()['id']
                self.created_ids['cervezas'].append(cerveza_id)
                self.print_success(f"Cerveza creada: {cerveza_data['nombre']} (ID: {cerveza_id})")
                return cerveza_id
            elif not expected_success and resp.status_code != 201:
                self.print_success(f"Creación fallida como se esperaba: {resp.status_code}")
                return None
            else:
                error_msg = resp.json().get('error', 'Error desconocido')
                self.print_error(f"Resultado inesperado. {resp.status_code} - {error_msg}")
                return None
                
        except Exception as e:
            self.print_error(f"Error creando cerveza: {e}")
            return None

    def test_buscar_cervezas(self, params=None, expected_min_count=0):
        """Prueba buscar cervezas - RF-3.1 y RF-5.7"""
        self.print_test_header("BUSCAR CERVEZAS")
        
        try:
            url = f"{BASE_URL}/cervezas/"
            if params:
                resp = requests.get(url, params=params)
            else:
                resp = requests.get(url)
            
            if resp.status_code == 200:
                cervezas = resp.json()
                if len(cervezas) >= expected_min_count:
                    self.print_success(f"Obtenidas {len(cervezas)} cervezas")
                    return cervezas
                else:
                    self.print_error(f"Se esperaban al menos {expected_min_count} cervezas, se obtuvieron {len(cervezas)}")
                    return cervezas
            else:
                error_msg = resp.json().get('error', 'Error desconocido')
                self.print_error(f"Error buscando cervezas. Código: {resp.status_code} - {error_msg}")
                return None
                
        except Exception as e:
            self.print_error(f"Error buscando cervezas: {e}")
            return None

    def test_obtener_detalle_cerveza(self, cerveza_id, expected_success=True):
        """Prueba obtener detalle de cerveza - RF-3.4"""
        self.print_test_header(f"OBTENER DETALLE DE CERVEZA: {cerveza_id}")
        
        try:
            resp = requests.get(f"{BASE_URL}/cervezas/{cerveza_id}/")
            
            if expected_success and resp.status_code == 200:
                detalle = resp.json()
                self.print_success(f"Cerveza obtenida: {detalle['nombre']}")
                return detalle
            elif not expected_success and resp.status_code == 404:
                self.print_success("Cerveza no encontrada (como se esperaba)")
                return None
            else:
                error_msg = resp.json().get('error', 'Error desconocido')
                self.print_error(f"Resultado inesperado. {resp.status_code} - {error_msg}")
                return None
                
        except Exception as e:
            self.print_error(f"Error obteniendo cerveza: {e}")
            return None

    def test_eliminar_cerveza(self, cerveza_id, expected_success=True):
        """Prueba eliminar cerveza"""
        self.print_test_header(f"ELIMINAR CERVEZA: {cerveza_id}")
        
        try:
            resp = requests.delete(f"{BASE_URL}/cervezas/{cerveza_id}/")
            
            if expected_success and resp.status_code == 200:
                self.print_success(f"Cerveza {cerveza_id} eliminada exitosamente")
                if cerveza_id in self.created_ids['cervezas']:
                    self.created_ids['cervezas'].remove(cerveza_id)
                return True
            elif not expected_success and resp.status_code == 404:
                self.print_success("Eliminación fallida como se esperaba (cerveza no existe)")
                return False
            else:
                error_msg = resp.json().get('error', 'Error desconocido')
                self.print_error(f"Resultado inesperado. {resp.status_code} - {error_msg}")
                return False
                
        except Exception as e:
            self.print_error(f"Error eliminando cerveza: {e}")
            return False

    def test_obtener_cervezas_favoritas(self, usuario_id, expected_success=True):
        """Prueba obtener cervezas favoritas de usuario - RF-5.4"""
        self.print_test_header(f"OBTENER CERVEZAS FAVORITAS DEL USUARIO: {usuario_id}")
        
        try:
            resp = requests.get(f"{BASE_URL}/usuarios/{usuario_id}/cervezas/favoritas/")
            
            if expected_success and resp.status_code == 200:
                favoritas = resp.json()
                self.print_success(f"Obtenidas {len(favoritas)} cervezas favoritas")
                # Mostrar detalles de las favoritas
                for i, fav in enumerate(favoritas, 1):
                    print(f"   🍺 #{i}: {fav['nombre']} - Valoración: {fav.get('valoracion_usuario', 'N/A')}")
                return favoritas
            elif not expected_success and resp.status_code == 404:
                self.print_success("Usuario no encontrado (como se esperaba)")
                return None
            else:
                error_msg = resp.json().get('error', 'Error desconocido')
                self.print_error(f"Resultado inesperado. {resp.status_code} - {error_msg}")
                return None
                
        except Exception as e:
            self.print_error(f"Error obteniendo cervezas favoritas: {e}")
            return None

    def test_obtener_estilos(self, expected_min_count=0):
        """Prueba obtener estilos únicos - RNF-4"""
        self.print_test_header("OBTENER ESTILOS ÚNICOS")
        
        try:
            resp = requests.get(f"{BASE_URL}/cervezas/estilos/")
            
            if resp.status_code == 200:
                estilos = resp.json()
                if len(estilos) >= expected_min_count:
                    self.print_success(f"Obtenidos {len(estilos)} estilos únicos: {', '.join(estilos)}")
                    return estilos
                else:
                    self.print_error(f"Se esperaban al menos {expected_min_count} estilos, se obtuvieron {len(estilos)}")
                    return estilos
            else:
                self.print_error(f"Error obteniendo estilos. Código: {resp.status_code}")
                return None
                
        except Exception as e:
            self.print_error(f"Error obteniendo estilos: {e}")
            return None

    def test_obtener_paises(self, expected_min_count=0):
        """Prueba obtener países únicos - RNF-4"""
        self.print_test_header("OBTENER PAÍSES ÚNICOS")
        
        try:
            resp = requests.get(f"{BASE_URL}/cervezas/paises/")
            
            if resp.status_code == 200:
                paises = resp.json()
                if len(paises) >= expected_min_count:
                    self.print_success(f"Obtenidos {len(paises)} países únicos: {', '.join(paises)}")
                    return paises
                else:
                    self.print_error(f"Se esperaban al menos {expected_min_count} países, se obtuvieron {len(paises)}")
                    return paises
            else:
                self.print_error(f"Error obteniendo países. Código: {resp.status_code}")
                return None
                
        except Exception as e:
            self.print_error(f"Error obteniendo países: {e}")
            return None

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

    def test_crear_cerveza_sin_nombre(self):
        """Prueba crear cerveza sin nombre (debería fallar)"""
        self.print_test_header("CREAR CERVEZA SIN NOMBRE")
        
        cerveza_data = {
            "estilo": "IPA",
            "pais_procedencia": "España",
            "porcentaje_alcohol": 6.5
        }
        
        try:
            resp = requests.post(f"{BASE_URL}/cervezas/", json=cerveza_data)
            
            if resp.status_code == 400:
                self.print_success("Error 400 recibido correctamente (nombre obligatorio)")
                return True
            else:
                self.print_error(f"Se esperaba 400 pero se recibió {resp.status_code}")
                return False
                
        except Exception as e:
            self.print_error(f"Error creando cerveza sin nombre: {e}")
            return False

    def test_buscar_cerveza_inexistente(self):
        """Prueba buscar cerveza que no existe"""
        self.print_test_header("BUSCAR CERVEZA INEXISTENTE")
        
        try:
            resp = requests.get(f"{BASE_URL}/cervezas/999999/")
            
            if resp.status_code == 404:
                self.print_success("Error 404 recibido correctamente (cerveza no existe)")
                return True
            else:
                self.print_error(f"Se esperaba 404 pero se recibió {resp.status_code}")
                return False
                
        except Exception as e:
            self.print_error(f"Error buscando cerveza inexistente: {e}")
            return False

    def test_busqueda_filtros_avanzados(self):
        """Prueba búsqueda con múltiples filtros"""
        self.print_test_header("BÚSQUEDA CON FILTROS AVANZADOS")
        
        params = {
            'q': 'ipa',
            'estilo': 'IPA',
            'pais': 'España'
        }
        
        try:
            cervezas = self.test_buscar_cervezas(params, expected_min_count=0)
            if cervezas is not None:
                self.print_success("Búsqueda con filtros ejecutada correctamente")
                return True
            else:
                return False
        except Exception as e:
            self.print_error(f"Error en búsqueda con filtros: {e}")
            return False

    def test_cervezas_favoritas_usuario_inexistente(self):
        """Prueba obtener cervezas favoritas de usuario inexistente"""
        self.print_test_header("CERVEZAS FAVORITAS DE USUARIO INEXISTISTENTE")
        
        try:
            resp = requests.get(f"{BASE_URL}/usuarios/999999/cervezas/favoritas/")
            
            if resp.status_code == 404:
                self.print_success("Error 404 recibido correctamente (usuario no existe)")
                return True
            else:
                self.print_error(f"Se esperaba 404 pero se recibió {resp.status_code}")
                return False
                
        except Exception as e:
            self.print_error(f"Error obteniendo favoritas de usuario inexistente: {e}")
            return False

    def crear_degustaciones_para_favoritas(self, usuario_id, cerveceria_id, cervezas_ids):
        """Crea degustaciones para probar el sistema de favoritas"""
        self.print_test_header("CREANDO DEGUSTACIONES PARA PRUEBA DE FAVORITAS")
        
        degustaciones_creadas = 0
        
        # Crear múltiples degustaciones con diferentes puntuaciones
        for i, cerveza_id in enumerate(cervezas_ids):
            # Asignar puntuaciones más altas a las primeras cervezas para que sean favoritas
            puntuacion = 5.0 - (i * 0.5)  # 5.0, 4.5, 4.0, etc.
            puntuacion = max(1.0, puntuacion)  # No menor que 1.0
            
            degustacion_id = self.test_crear_degustacion(
                usuario_id=usuario_id,
                cerveza_id=cerveza_id,
                cerveceria_id=cerveceria_id,
                puntuacion=puntuacion 
            )
            
            if degustacion_id:
                degustaciones_creadas += 1
                print(f"   🍻 Degustación creada: Cerveza {cerveza_id} - Puntuación: {puntuacion}")
            self.wait_for_operation(0.2)
        
        self.print_success(f"Creadas {degustaciones_creadas} degustaciones de prueba")
        return degustaciones_creadas
    
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
                self.print_error(f"Resultado inesperado. {resp.status_code} - {resp.text}")
                return None
                
        except Exception as e:
            error_msg = resp.json().get('error', 'Error desconocido')
            self.print_error(f"Resultado inesperado. {resp.status_code} - {error_msg}")

    def run_comprehensive_test(self):
        """Ejecuta una prueba completa de todos los endpoints de cervezas"""
        self.print_test_header("INICIANDO PRUEBA COMPREHENSIVA DE CERVEZAS")
        
        # Paso 0: Verificar servidor
        self.print_info("Paso 0: Verificando conexión al servidor...")
        if not self.test_servidor_conectado():
            return
        
        # Paso 1: Crear usuario y cervecería de prueba
        self.print_info("Paso 1: Creando usuario y cervecería de prueba...")
        usuario_id = self.crear_usuario_prueba("test_cerveza")
        if not usuario_id:
            self.print_error("No se pudo crear usuario de prueba. Abortando prueba.")
            return
        self.wait_for_operation()

        cerveceria_id = self.test_crear_cerveceria("test_cerveceria", "Madrid")
        if not cerveceria_id:
            self.print_error("No se pudo crear cervecería de prueba. Abortando prueba.")
            return
        self.wait_for_operation()
        
        # Paso 2: Crear cervezas de prueba
        self.print_info("Paso 2: Creando cervezas de prueba...")
        
        cervezas_test = [
            {
                "nombre": "IPA Artesanal Test",
                "estilo": "IPA",
                "pais_procedencia": "España",
                "porcentaje_alcohol": 6.5,
                "descripcion": "Una IPA artesanal de prueba"
            },
            {
                "nombre": "Stout Imperial Test", 
                "estilo": "Stout",
                "pais_procedencia": "Irlanda",
                "porcentaje_alcohol": 8.2,
                "descripcion": "Stout imperial de prueba"
            },
            {
                "nombre": "Pilsner Checa Test",
                "estilo": "Pilsner", 
                "pais_procedencia": "República Checa",
                "porcentaje_alcohol": 5.0,
                "descripcion": "Pilsner tradicional checa"
            },
            {
                "nombre": "Amber Ale Test",
                "estilo": "Amber Ale",
                "pais_procedencia": "Alemania",
                "porcentaje_alcohol": 5.5,
                "descripcion": "Amber Ale de prueba"
            },
            {
                "nombre": "Wheat Beer Test",
                "estilo": "Wheat Beer", 
                "pais_procedencia": "Bélgica",
                "porcentaje_alcohol": 4.8,
                "descripcion": "Wheat Beer de prueba"
            }
        ]
        
        cervezas_ids = []
        for cerveza_data in cervezas_test:
            cerveza_id = self.test_crear_cerveza(cerveza_data)
            if cerveza_id:
                cervezas_ids.append(cerveza_id)
            self.wait_for_operation()
        
        if len(cervezas_ids) < 3:
            self.print_error("No se pudieron crear suficientes cervezas de prueba. Abortando prueba.")
            self.cleanup()
            return
        
        # Paso 3: Crear degustaciones para probar favoritas
        self.print_info("Paso 3: Creando degustaciones para sistema de favoritas...")
        self.crear_degustaciones_para_favoritas(usuario_id, cerveceria_id, cervezas_ids)
        self.wait_for_operation(1)  # Esperar un poco más para que se procesen las degustaciones
        
        # Paso 4: Probar obtención de cervezas
        self.print_info("Paso 4: Probando obtención de cervezas...")
        self.test_obtener_detalle_cerveza(cervezas_ids[0])
        self.wait_for_operation()
        
        self.test_buscar_cervezas(expected_min_count=len(cervezas_ids))
        self.wait_for_operation()
        
        # Paso 5: Probar búsquedas y filtros
        self.print_info("Paso 5: Probando búsquedas y filtros...")
        self.test_buscar_cervezas({'q': 'IPA'}, expected_min_count=1)
        self.wait_for_operation()
        
        self.test_buscar_cervezas({'estilo': 'Stout'}, expected_min_count=1)
        self.wait_for_operation()
        
        self.test_buscar_cervezas({'pais': 'España'}, expected_min_count=1)
        self.wait_for_operation()
        
        self.test_busqueda_filtros_avanzados()
        self.wait_for_operation()
        
        # Paso 6: Probar endpoints de listas únicas
        self.print_info("Paso 6: Probando listas únicas...")
        self.test_obtener_estilos(expected_min_count=len(set(c['estilo'] for c in cervezas_test)))
        self.wait_for_operation()
        
        self.test_obtener_paises(expected_min_count=len(set(c['pais_procedencia'] for c in cervezas_test)))
        self.wait_for_operation()
        
        # Paso 7: Probar cervezas favoritas (¡AHORA CON DATOS REALES!)
        self.print_info("Paso 7: Probando cervezas favoritas con datos reales...")
        favoritas = self.test_obtener_cervezas_favoritas(usuario_id, expected_success=True)
        
        # Verificar que las favoritas estén ordenadas correctamente
        if favoritas and len(favoritas) > 0:
            self.print_success("✅ Sistema de favoritas funcionando correctamente")
            # Las cervezas con puntuaciones más altas deberían aparecer primero
            puntuaciones = [fav.get('valoracion_usuario', 0) for fav in favoritas]
            if all(puntuaciones[i] >= puntuaciones[i+1] for i in range(len(puntuaciones)-1)):
                self.print_success("✅ Favoritas correctamente ordenadas por valoración")
            else:
                self.print_error("❌ Las favoritas no están ordenadas correctamente")
        
        self.wait_for_operation()
        
        # Paso 8: Probar casos de error
        self.print_info("Paso 8: Probando casos de error...")
        self.test_obtener_detalle_cerveza(999999, expected_success=False)
        self.wait_for_operation()
        
        self.test_crear_cerveza_sin_nombre()
        self.wait_for_operation()
        
        self.test_cervezas_favoritas_usuario_inexistente()
        self.wait_for_operation()
        
        # Paso 9: Probar eliminación
        self.print_info("Paso 9: Probando eliminación de cervezas...")
        if self.created_ids['cervezas']:
            cerveza_a_eliminar = self.created_ids['cervezas'][0]
            self.test_eliminar_cerveza(cerveza_a_eliminar)
            self.wait_for_operation()
        
        # Resultados finales
        self.print_test_summary()

    def run_quick_test(self):
        """Ejecuta una prueba rápida con datos existentes"""
        self.print_test_header("INICIANDO PRUEBA RÁPIDA DE CERVEZAS")
        
        # Verificar servidor
        if not self.test_servidor_conectado():
            return
        
        # Probar endpoints básicos con datos existentes
        self.test_buscar_cervezas()
        self.wait_for_operation()
        
        self.test_obtener_estilos()
        self.wait_for_operation()
        
        self.test_obtener_paises()
        self.wait_for_operation()
        
        # Si hay cervezas, probar obtener una específica
        cervezas = self.test_buscar_cervezas()
        if cervezas and len(cervezas) > 0:
            primera_cerveza_id = cervezas[0]['id']
            self.test_obtener_detalle_cerveza(primera_cerveza_id)
            self.wait_for_operation()
        
        # Probar cervezas favoritas con usuario existente
        self.test_obtener_cervezas_favoritas(1)
        self.wait_for_operation()
        
        self.print_test_summary()

    def print_test_summary(self):
        """Imprime un resumen de los resultados de las pruebas"""
        self.print_test_header("RESUMEN DE PRUEBAS DE CERVEZAS")
        print(f"✅ Pruebas exitosas: {self.test_results['passed']}")
        print(f"❌ Pruebas fallidas: {self.test_results['failed']}")
        print(f"📊 Total de pruebas: {self.total_tests}")
        
        if self.test_results['errors']:
            print(f"\n🔍 Errores encontrados:")
            for error in self.test_results['errors']:
                print(f"   - {error}")
        
        success_pct = self.get_success_percentage()
        print(f"\n🎯 Tasa de éxito: {success_pct:.1f}%")
        
        # Mostrar cobertura de endpoints probados
        endpoints_probados = [
            "POST /cervezas/ (RF-3.2)",
            "GET /cervezas/ (RF-3.1, RF-5.7)", 
            "GET /cervezas/{id}/ (RF-3.4)",
            "DELETE /cervezas/{id}/",
            "GET /usuarios/{id}/cervezas/favoritas/ (RF-5.4)",
            "GET /cervezas/estilos/ (RNF-4)",
            "GET /cervezas/paises/ (RNF-4)",
            "POST /usuarios/ (para pruebas)",
            "POST /degustaciones/ (para pruebas)"
        ]
        
        print(f"\n📋 Endpoints probados:")
        for endpoint in endpoints_probados:
            print(f"   • {endpoint}")
        
        if self.test_results['failed'] == 0 and self.test_results['passed'] > 0:
            print("\n🎉 ¡TODAS LAS PRUEBAS DE CERVEZAS EXITOSAS!")
        elif self.test_results['passed'] > 0:
            print("\n⚠️  Algunas pruebas fallaron, pero otras fueron exitosas")
        else:
            print("\n💥 Todas las pruebas fallaron")

# --- Ejecución de pruebas ---
if __name__ == "__main__":
    tester = CervezaTester()
    
    print("Iniciando pruebas de API de Cervezas...")
    print("Asegúrate de que el servidor Flask esté ejecutándose en http://localhost:8000")
    time.sleep(2)
    
    # Ejecutar prueba comprehensiva (crea y elimina datos de prueba)
    tester.run_comprehensive_test()
    
    # O ejecutar prueba rápida (usa datos existentes)
    # tester.run_quick_test()
    
    # Limpieza final
    tester.cleanup()