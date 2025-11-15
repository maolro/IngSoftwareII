import requests
import json
import time
import random

# --- Configuración ---
BASE_URL = "http://localhost:8000/api"

class DegustacionTester:
    """Clase para realizar pruebas automatizadas de los endpoints de degustaciones"""
    
    def __init__(self):
        self.created_ids = {
            'degustaciones': [],
            'usuarios': [],
            'cervezas': [],
            'cervecerias': [],
            'comentarios': []
        }
        self.test_results = {
            'passed': 0,
            'failed': 0,
            'errors': []
        }
    
    def print_test_header(self, titulo):
        """Imprime un cabezal bonito para cada prueba"""
        print("\n" + "="*60)
        print(f" PRUEBA: {titulo}")
        print("="*60)
    
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
        print(f"\nℹ️  {message}")
    
    def wait_for_operation(self, seconds=0.5):
        """Wait between operations to avoid race conditions"""
        time.sleep(seconds)

    def cleanup(self):
        """Limpia todos los datos creados durante las pruebas"""
        self.print_test_header("LIMPIANDO DATOS DE PRUEBA")
        
        cleanup_count = 0
        
        # Limpiar comentarios
        for comentario_id in self.created_ids['comentarios'][:]:
            try:
                # Asumiendo que hay un endpoint para eliminar comentarios
                resp = requests.delete(f"{BASE_URL}/comentarios/{comentario_id}")
                if resp.status_code in [200, 204]:
                    print(f"✅ Comentario eliminado: {comentario_id}")
                    self.created_ids['comentarios'].remove(comentario_id)
                    cleanup_count += 1
            except Exception as e:
                print(f"⚠️  Error eliminando comentario {comentario_id}: {e}")
        
        # Limpiar degustaciones
        for degustacion_id in self.created_ids['degustaciones'][:]:
            try:
                resp = requests.delete(f"{BASE_URL}/degustaciones/{degustacion_id}")
                if resp.status_code == 200:
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
                resp = requests.delete(f"{BASE_URL}/cervezas/{cerveza_id}")
                if resp.status_code in [200, 204]:
                    print(f"✅ Cerveza eliminada: {cerveza_id}")
                    self.created_ids['cervezas'].remove(cerveza_id)
                    cleanup_count += 1
            except Exception as e:
                print(f"⚠️  Error eliminando cerveza {cerveza_id}: {e}")
        
        # Limpiar cervecerías
        for cerveceria_id in self.created_ids['cervecerias'][:]:
            try:
                resp = requests.delete(f"{BASE_URL}/cervecerias/{cerveceria_id}")
                if resp.status_code in [200, 204]:
                    print(f"✅ Cervecería eliminada: {cerveceria_id}")
                    self.created_ids['cervecerias'].remove(cerveceria_id)
                    cleanup_count += 1
            except Exception as e:
                print(f"⚠️  Error eliminando cervecería {cerveceria_id}: {e}")
        
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

    def crear_usuario_prueba(self, username=""):
        """Crea un usuario de prueba para las degustaciones"""
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
                self.print_success(f"Usuario de prueba creado: {usuario_id}")
                return usuario_id
            else:
                self.print_error(f"Error creando usuario: {resp.status_code} - {resp.json()['error']}")
                return None
        except Exception as e:
            self.print_error(f"Error creando usuario: {e}")
            return None

    def crear_cerveza_prueba(self, nombre_suffix=""):
        """Crea una cerveza de prueba"""
        cerveza_data = {
            "nombre": f"Cerveza Test {nombre_suffix}",
            "estilo": random.choice(["IPA", "Stout", "Lager", "Pilsen", "Weiss"]),
            "pais_procedencia": random.choice(["España", "Alemania", "Bélgica", "EEUU", "Reino Unido"]),
            "tamaño": "330ml",
            "formato": "Botella",
            "alcohol": round(random.uniform(4.0, 8.0), 1),
            "amargor": random.randint(10, 80),
            "color": "Dorado",
            "descripcion": f"Cerveza de prueba {nombre_suffix} para testing"
        }
        
        try:
            resp = requests.post(f"{BASE_URL}/cervezas/", json=cerveza_data)
            if resp.status_code == 201:
                cerveza_id = resp.json()['id']
                self.created_ids['cervezas'].append(cerveza_id)
                self.print_success(f"Cerveza de prueba creada: {cerveza_id}")
                return cerveza_id
            else:
                self.print_error(f"Error creando cerveza: {resp.status_code} - {resp.json()['error']}")
                return None
        except Exception as e:
            self.print_error(f"Error creando cerveza: {e}")
            return None

    def crear_cerveceria_prueba(self, nombre_suffix=""):
        """Crea una cervecería de prueba"""
        cerveceria_data = {
            "nombre": f"Cervecería Test {nombre_suffix}",
            "direccion": f"Calle Test {random.randint(1, 100)}, Ciudad Test",
            "latitud": round(random.uniform(40.0, 41.0), 6),
            "longitud": round(random.uniform(-3.5, -3.0), 6)
        }
        
        try:
            resp = requests.post(f"{BASE_URL}/cervecerias/", json=cerveceria_data)
            if resp.status_code == 201:
                cerveceria_id = resp.json()['id']
                self.created_ids['cervecerias'].append(cerveceria_id)
                self.print_success(f"Cervecería de prueba creada: {cerveceria_id}")
                return cerveceria_id
            else:
                self.print_error(f"Error creando cervecería: {resp.status_code} - {resp.json()['error']}")
                return None
        except Exception as e:
            self.print_error(f"Error creando cervecería: {e}")
            return None

    def test_crear_degustacion(self, usuario_id, cerveza_id, cerveceria_id=None, expected_success=True):
        """Prueba para crear degustación"""
        degustacion_data = {
            "usuario_id": usuario_id,
            "cerveza_id": cerveza_id,
            "puntuacion": round(random.uniform(1.0, 5.0), 1),
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
                self.print_error(f"Resultado inesperado. {resp.status_code} - {resp.json()['error']}")
                return None
                
        except Exception as e:
            self.print_error(f"Error creando degustación: {e}")
            return None

    def test_obtener_degustacion_por_id(self, degustacion_id, expected_success=True):
        """Prueba obtener degustación por ID"""
        self.print_test_header(f"OBTENER DEGUSTACIÓN POR ID: {degustacion_id}")
        
        try:
            resp = requests.get(f"{BASE_URL}/degustaciones/{degustacion_id}/")
            
            if expected_success and resp.status_code == 200:
                detalle = resp.json()
                self.print_success(f"Degustación obtenida: ID {detalle['id']} - Puntuación: {detalle.get('puntuacion', 'Sin puntuar')}")
                return detalle
            elif not expected_success and resp.status_code == 404:
                self.print_success("Degustación no encontrada (como se esperaba)")
                return None
            else:
                self.print_error(f"Resultado inesperado. {resp.status_code} - {resp.json()['error']}")
                return None
                
        except Exception as e:
            self.print_error(f"Error obteniendo degustación: {e}")
            return None

    def test_obtener_degustaciones_por_usuario(self, usuario_id, expected_min_count=0):
        """Prueba obtener degustaciones por usuario"""
        self.print_test_header(f"OBTENER DEGUSTACIONES DE USUARIO: {usuario_id}")
        
        try:
            resp = requests.get(f"{BASE_URL}/degustaciones/", params={"usuario_id": usuario_id})
            
            if resp.status_code == 200:
                degustaciones = resp.json()
                if len(degustaciones) >= expected_min_count:
                    self.print_success(f"Obtenidas {len(degustaciones)} degustaciones del usuario")
                    return degustaciones
                else:
                    self.print_error(f"Se esperaban al menos {expected_min_count} degustaciones, se obtuvieron {len(degustaciones)}")
                    return degustaciones
            else:
                self.print_error(f"Error obteniendo degustaciones. Código: {resp.status_code} - {resp.json()['error']}")
                return None
                
        except Exception as e:
            self.print_error(f"Error obteniendo degustaciones: {e}")
            return None

    def test_obtener_degustaciones_por_cerveza(self, cerveza_id, expected_min_count=0):
        """Prueba obtener degustaciones por cerveza"""
        self.print_test_header(f"OBTENER DEGUSTACIONES DE CERVEZA: {cerveza_id}")
        
        try:
            resp = requests.get(f"{BASE_URL}/degustaciones/", params={"cerveza_id": cerveza_id})
            
            if resp.status_code == 200:
                degustaciones = resp.json()
                if len(degustaciones) >= expected_min_count:
                    self.print_success(f"Obtenidas {len(degustaciones)} degustaciones de la cerveza")
                    return degustaciones
                else:
                    self.print_error(f"Se esperaban al menos {expected_min_count} degustaciones, se obtuvieron {len(degustaciones)}")
                    return degustaciones
            else:
                self.print_error(f"Error obteniendo degustaciones. Código: {resp.status_code} - {resp.json()['error']}")
                return None
                
        except Exception as e:
            self.print_error(f"Error obteniendo degustaciones: {e}")
            return None

    def test_actualizar_degustacion(self, degustacion_id, nuevos_datos, expected_success=True):
        """Prueba actualizar degustación"""
        self.print_test_header(f"ACTUALIZAR DEGUSTACIÓN: {degustacion_id}")
        
        try:
            resp = requests.put(f"{BASE_URL}/degustaciones/{degustacion_id}/", json=nuevos_datos)
            
            if expected_success and resp.status_code == 200:
                degustacion_actualizada = resp.json()
                self.print_success(f"Degustación actualizada: ID {degustacion_actualizada['id']}")
                return degustacion_actualizada
            elif not expected_success and resp.status_code != 200:
                self.print_success("Actualización fallida como se esperaba")
                return None
            else:
                self.print_error(f"Resultado inesperado. {resp.status_code} - {resp.json()['error']}")
                return None
                
        except Exception as e:
            self.print_error(f"Error actualizando degustación: {e}")
            return None

    def test_eliminar_degustacion(self, degustacion_id, expected_success=True):
        """Prueba eliminar degustación"""
        self.print_test_header(f"ELIMINAR DEGUSTACIÓN: {degustacion_id}")
        
        try:
            resp = requests.delete(f"{BASE_URL}/degustaciones/{degustacion_id}")
            
            if expected_success and resp.status_code == 200:
                self.print_success(f"Degustación {degustacion_id} eliminada exitosamente")
                if degustacion_id in self.created_ids['degustaciones']:
                    self.created_ids['degustaciones'].remove(degustacion_id)
                return True
            elif not expected_success and resp.status_code == 404:
                self.print_success("Eliminación fallida como se esperaba (degustación no existe)")
                return False
            else:
                self.print_error(f"Resultado inesperado. {resp.status_code} - {resp.json()['error']}")
                return False
                
        except Exception as e:
            self.print_error(f"Error eliminando degustación: {e}")
            return False

    def test_obtener_degustaciones_mas_valoradas(self, estilo=None, pais=None):
        """Prueba obtener degustaciones más valoradas con filtros"""
        self.print_test_header("OBTENER DEGUSTACIONES MÁS VALORADAS")
        
        try:
            params = {}
            if estilo:
                params['estilo'] = estilo
            if pais:
                params['pais'] = pais
                
            resp = requests.get(f"{BASE_URL}/degustaciones/mas-valoradas/", params=params)
            
            if resp.status_code == 200:
                degustaciones = resp.json()
                self.print_success(f"Obtenidas {len(degustaciones)} degustaciones más valoradas")
                if estilo or pais:
                    self.print_info(f"Filtros aplicados: estilo={estilo}, pais={pais}")
                return degustaciones
            else:
                self.print_error(f"Error obteniendo degustaciones más valoradas. {resp.status_code} - {resp.json()['error']}")
                return None
                
        except Exception as e:
            self.print_error(f"Error obteniendo degustaciones más valoradas: {e}")
            return None

    def test_agregar_comentario_degustacion(self, degustacion_id, usuario_id, comentario, expected_success=True):
        """Prueba agregar comentario a degustación"""
        self.print_test_header(f"AGREGAR COMENTARIO A DEGUSTACIÓN: {degustacion_id}")
        
        comentario_data = {
            "degustacion_id": degustacion_id,
            "usuario_id": usuario_id,
            "comentario": comentario
        }
        
        try:
            resp = requests.post(f"{BASE_URL}/degustaciones/{degustacion_id}/comentarios/", json=comentario_data)
            
            if expected_success and resp.status_code == 201:
                comentario_id = resp.json()['id']
                self.created_ids['comentarios'].append(comentario_id)
                self.print_success(f"Comentario agregado: ID {comentario_id}")
                return comentario_id
            elif not expected_success and resp.status_code != 201:
                self.print_success("Agregar comentario falló como se esperaba")
                return None
            else:
                self.print_error(f"Resultado inesperado. {resp.status_code} - {resp.json()['error']}")
                return None
                
        except Exception as e:
            self.print_error(f"Error agregando comentario: {e}")
            return None

    def test_obtener_comentarios_degustacion(self, degustacion_id, expected_min_count=0):
        """Prueba obtener comentarios de degustación"""
        self.print_test_header(f"OBTENER COMENTARIOS DE DEGUSTACIÓN: {degustacion_id}")
        
        try:
            resp = requests.get(f"{BASE_URL}/degustaciones/{degustacion_id}/comentarios/")
            
            if resp.status_code == 200:
                comentarios = resp.json()
                if len(comentarios) >= expected_min_count:
                    self.print_success(f"Obtenidos {len(comentarios)} comentarios de la degustación")
                    return comentarios
                else:
                    self.print_error(f"Se esperaban al menos {expected_min_count} comentarios, se obtuvieron {len(comentarios)}")
                    return comentarios
            else:
                self.print_error(f"Error obteniendo comentarios. {resp.status_code} - {resp.json()['error']}")
                return None
                
        except Exception as e:
            self.print_error(f"Error obteniendo comentarios: {e}")
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

    def test_degustacion_sin_puntuacion(self, usuario_id, cerveza_id):
        """Prueba crear degustación sin puntuación (RF-3.3)"""
        self.print_test_header("CREAR DEGUSTACIÓN SIN PUNTUACIÓN")
        
        degustacion_data = {
            "usuario_id": usuario_id,
            "cerveza_id": cerveza_id,
            "comentario": "Degustación sin puntuación - solo comentario"
        }
        
        try:
            resp = requests.post(f"{BASE_URL}/degustaciones/", json=degustacion_data)
            
            if resp.status_code == 201:
                degustacion_id = resp.json()['id']
                self.created_ids['degustaciones'].append(degustacion_id)
                self.print_success(f"Degustación sin puntuación creada: ID {degustacion_id}")
                return degustacion_id
            else:
                self.print_error(f"Error creando degustación sin puntuación: {resp.status_code} - {resp.json()['error']}")
                return None
                
        except Exception as e:
            self.print_error(f"Error creando degustación sin puntuación: {e}")
            return None

    def test_puntuacion_invalida(self, usuario_id, cerveza_id):
        """Prueba crear degustación con puntuación inválida"""
        self.print_test_header("CREAR DEGUSTACIÓN CON PUNTUACIÓN INVÁLIDA")
        
        degustacion_data = {
            "usuario_id": usuario_id,
            "cerveza_id": cerveza_id,
            "puntuacion": 6.0,  # Puntuación fuera de rango
            "comentario": "Esta debería fallar"
        }
        
        try:
            resp = requests.post(f"{BASE_URL}/degustaciones/", json=degustacion_data)
            
            if resp.status_code == 400:
                self.print_success("Error 400 recibido correctamente (puntuación inválida)")
                return True
            else:
                self.print_error(f"Se esperaba 400 pero se recibió {resp.status_code}")
                return False
                
        except Exception as e:
            self.print_error(f"Error probando puntuación inválida: {e}")
            return False

    def run_comprehensive_test(self):
        """Ejecuta una prueba completa de todos los endpoints de degustaciones"""
        self.print_test_header("INICIANDO PRUEBA COMPREHENSIVA DE DEGUSTACIONES")
        
        # Paso 0: Verificar servidor
        self.print_info("Paso 0: Verificando conexión al servidor...")
        if not self.test_servidor_conectado():
            return
        
        # Paso 1: Crear datos de prueba
        self.print_info("Paso 1: Creando datos de prueba...")
        
        usuario1_id = self.crear_usuario_prueba("degustador1")
        usuario2_id = self.crear_usuario_prueba("degustador2")
        self.wait_for_operation()
        
        cerveza1_id = self.crear_cerveza_prueba("IPA Premium")
        cerveza2_id = self.crear_cerveza_prueba("Stout Imperial")
        cerveza3_id = self.crear_cerveza_prueba("Lager Clásica")
        self.wait_for_operation()
        
        cerveceria1_id = self.crear_cerveceria_prueba("Centro")
        cerveceria2_id = self.crear_cerveceria_prueba("Norte")
        self.wait_for_operation()
        
        if not all([usuario1_id, cerveza1_id, cerveza2_id]):
            self.print_error("No se pudieron crear datos de prueba básicos. Abortando prueba.")
            self.cleanup()
            return
        
        # Paso 2: Probar creación de degustaciones
        self.print_info("Paso 2: Probando creación de degustaciones...")
        
        degustacion1_id = self.test_crear_degustacion(usuario1_id, cerveza1_id, cerveceria1_id)
        self.wait_for_operation()
        
        degustacion2_id = self.test_crear_degustacion(usuario1_id, cerveza2_id)
        self.wait_for_operation()
        
        degustacion3_id = self.test_crear_degustacion(usuario2_id, cerveza1_id, cerveceria2_id)
        self.wait_for_operation()
        
        # Paso 3: Probar casos especiales de degustaciones
        self.print_info("Paso 3: Probando casos especiales...")
        
        self.test_degustacion_sin_puntuacion(usuario1_id, cerveza3_id)
        self.wait_for_operation()
        
        self.test_puntuacion_invalida(usuario2_id, cerveza2_id)
        self.wait_for_operation()
        
        # Paso 4: Probar obtención de degustaciones
        self.print_info("Paso 4: Probando obtención de degustaciones...")
        
        self.test_obtener_degustacion_por_id(degustacion1_id)
        self.wait_for_operation()
        
        self.test_obtener_degustaciones_por_usuario(usuario1_id, expected_min_count=3)
        self.wait_for_operation()
        
        self.test_obtener_degustaciones_por_cerveza(cerveza1_id, expected_min_count=2)
        self.wait_for_operation()
        
        # Paso 5: Probar degustaciones más valoradas
        self.print_info("Paso 5: Probando degustaciones más valoradas...")
        
        self.test_obtener_degustaciones_mas_valoradas()
        self.wait_for_operation()
        
        self.test_obtener_degustaciones_mas_valoradas(estilo="IPA")
        self.wait_for_operation()
        
        # Paso 6: Probar comentarios en degustaciones
        self.print_info("Paso 6: Probando comentarios en degustaciones...")
        
        comentario1_id = self.test_agregar_comentario_degustacion(
            degustacion1_id, usuario2_id, 
            "¡Excelente degustación! Estoy de acuerdo con tu opinión."
        )
        self.wait_for_operation()
        
        comentario2_id = self.test_agregar_comentario_degustacion(
            degustacion1_id, usuario1_id, 
            "Gracias por tu comentario. ¡Salud!"
        )
        self.wait_for_operation()
        
        self.test_obtener_comentarios_degustacion(degustacion1_id, expected_min_count=2)
        self.wait_for_operation()
        
        # Paso 7: Probar actualización de degustaciones
        self.print_info("Paso 7: Probando actualización de degustaciones...")
        
        self.test_actualizar_degustacion(
            degustacion2_id,
            {
                "puntuacion": 4.5,
                "comentario": "Comentario actualizado después de una segunda cata"
            }
        )
        self.wait_for_operation()
        
        # Paso 8: Probar casos de error
        self.print_info("Paso 8: Probando casos de error...")
        
        self.test_obtener_degustacion_por_id(99999, expected_success=False)
        self.wait_for_operation()
        
        # Paso 9: Probar eliminación
        self.print_info("Paso 9: Probando eliminación de degustaciones...")
        
        if self.created_ids['degustaciones']:
            degustacion_a_eliminar = self.created_ids['degustaciones'][0]
            self.test_eliminar_degustacion(degustacion_a_eliminar)
            self.wait_for_operation()
        
        # Resultados finales
        self.print_test_summary()

    def run_quick_test(self):
        """Ejecuta una prueba rápida con datos existentes"""
        self.print_test_header("INICIANDO PRUEBA RÁPIDA DE DEGUSTACIONES")
        
        # Verificar servidor
        if not self.test_servidor_conectado():
            return
        
        # Probar endpoints básicos
        self.test_obtener_degustaciones_mas_valoradas()
        self.wait_for_operation()
        
        # Si hay usuarios, probar obtener sus degustaciones
        usuario_prueba = self.crear_usuario_prueba("_quick_test")
        if usuario_prueba:
            self.test_obtener_degustaciones_por_usuario(usuario_prueba)
            self.wait_for_operation()
        
        self.print_test_summary()

    def print_test_summary(self):
        """Imprime un resumen de los resultados de las pruebas"""
        self.print_test_header("RESUMEN DE PRUEBAS DE DEGUSTACIONES")
        print(f"✅ Pruebas exitosas: {self.test_results['passed']}")
        print(f"❌ Pruebas fallidas: {self.test_results['failed']}")
        print(f"📊 Total de pruebas: {self.test_results['passed'] + self.test_results['failed']}")
        
        if self.test_results['errors']:
            print(f"\n🔍 Errores encontrados:")
            for error in self.test_results['errors']:
                print(f"   - {error}")
        
        total_tests = self.test_results['passed'] + self.test_results['failed']
        if total_tests > 0:
            success_rate = (self.test_results['passed'] / total_tests) * 100
            print(f"\n🎯 Tasa de éxito: {success_rate:.1f}%")
        
        if self.test_results['failed'] == 0 and self.test_results['passed'] > 0:
            print("\n🎉 ¡TODAS LAS PRUEBAS DE DEGUSTACIONES EXITOSAS!")
        elif self.test_results['passed'] > 0:
            print("\n⚠️  Algunas pruebas fallaron, pero otras fueron exitosas")
        else:
            print("\n💥 Todas las pruebas fallaron")

# --- Ejecución de pruebas ---
if __name__ == "__main__":
    tester = DegustacionTester()
    
    print("Iniciando pruebas de API de Degustaciones...")
    print("Asegúrate de que el servidor Flask esté ejecutándose en http://localhost:8000")
    time.sleep(2)
    
    # Ejecutar prueba comprehensiva (crea y elimina datos de prueba)
    tester.run_comprehensive_test()
    
    # O ejecutar prueba rápida (usa datos existentes)
    # tester.run_quick_test()
    
    # Limpieza final
    tester.cleanup()