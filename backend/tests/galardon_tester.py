import requests
import json
import time

# --- Configuración ---
BASE_URL = "http://localhost:8000/api"

class GalardonTester:
    """Clase para realizar pruebas automatizadas de los endpoints de galardones"""
    
    def __init__(self):
        self.created_ids = {
            'galardones': [],
            'usuarios': [],
            'usuarios_galardones': []  # Para trackear asignaciones
        }
        self.test_results = {
            'passed': 0,
            'failed': 0,
            'errors': []
        }
    
    def print_test_header(self, titulo):
        """ Imprime un cabezal bonito para cada prueba """
        print("\n" + "="*50)
        print(f" PRUEBA: {titulo}")
        print("="*50)
    
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
        print("\n" + "="*50+"\n")
        print(f"ℹ️  {message}")
    
    def wait_for_operation(self, seconds=0.5):
        """Wait between operations to avoid race conditions"""
        time.sleep(seconds)

    def cleanup(self):
        """ Limpia todos los datos creados durante las pruebas """
        self.print_test_header("LIMPIANDO DATOS DE PRUEBA")
        
        cleanup_count = 0
        
        # Limpiar asignaciones de galardones a usuarios primero
        for usuario_galardon_id in self.created_ids['usuarios_galardones'][:]:
            try:
                resp = requests.delete(f"{BASE_URL}/usuarios/{usuario_galardon_id[0]}/galardones/{usuario_galardon_id[1]}/")
                if resp.status_code == 200:
                    print(f"✅ Asignación eliminada: {usuario_galardon_id}")
                    self.created_ids['usuarios_galardones'].remove(usuario_galardon_id)
                    cleanup_count += 1
                else:
                    print(f"⚠️  No se pudo eliminar asignación {usuario_galardon_id}: {resp.json()['error']}")
            except Exception as e:
                print(f"❌ Error eliminando asignación {usuario_galardon_id}: {e}")
        
        # Limpiar galardones
        for galardon_id in self.created_ids['galardones'][:]:
            try:
                resp = requests.delete(f"{BASE_URL}/galardones/{galardon_id}")
                if resp.status_code == 200:
                    print(f"✅ Galardón eliminado: {galardon_id}")
                    self.created_ids['galardones'].remove(galardon_id)
                    cleanup_count += 1
                else:
                    print(f"⚠️  No se pudo eliminar galardón {galardon_id}: {resp.json()['error']}")
            except Exception as e:
                print(f"❌ Error eliminando galardón {galardon_id}: {e}")
        
        # Limpiar usuarios (si los creaste)
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
        """ Crea un usuario de prueba para los galardones """
        username = f"galardon_test_user{username_suffix}"
        usuario_data = {
            "username": username,
            "email": f"galardon_test{username_suffix}@test.com",
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
                self.print_error(f"Error creando usuario: {resp.status_code} - {resp.text}")
                return None
        except Exception as e:
            self.print_error(f"Error creando usuario: {e}")
            return None

    def test_asignar_galardon_a_usuario(self, usuario_id, galardon_id, fecha_obtencion=None):
        """Prueba para asignar un galardón a un usuario"""
        self.print_test_header(f"ASIGNAR GALARDÓN A USUARIO (Usuario: {usuario_id}, Galardón: {galardon_id})")
        
        if not fecha_obtencion:
            fecha_obtencion = time.strftime("%Y-%m-%d")
        
        asignacion_data = {
            "usuario_id": usuario_id,
            "galardon_id": galardon_id,
            "fecha_obtencion": fecha_obtencion
        }
        
        try:
            resp = requests.post(f"{BASE_URL}/usuarios/{usuario_id}/galardones", json=asignacion_data)
            
            if resp.status_code == 201:
                galardon_id = resp.json()['galardon_id']
                self.created_ids['usuarios_galardones'].append([usuario_id, galardon_id])
                self.print_success(f"Galardón {galardon_id} asignado al usuario {usuario_id}")
                return galardon_id
            else:
                self.print_error(f"Error asignando galardón: {resp.status_code} - {resp.text}")
                return None
                
        except Exception as e:
            self.print_error(f"Error asignando galardón: {e}")
            return None

    def test_verificar_galardones_usuario(self, usuario_id, galardones_esperados=None):
        """Verifica que un usuario tenga los galardones esperados"""
        self.print_test_header(f"VERIFICAR GALARDONES DE USUARIO: {usuario_id}")
        
        try:
            resp = requests.get(f"{BASE_URL}/usuarios/{usuario_id}/galardones/")
            
            if resp.status_code == 200:
                galardones_obtenidos = resp.json()
                
                # Si no se especifican galardones esperados, solo mostrar los obtenidos
                if galardones_esperados is None:
                    self.print_success(f"Usuario tiene {len(galardones_obtenidos)} galardones")
                    for galardon in galardones_obtenidos:
                        print(f"   - {galardon.get('nombre', 'Sin nombre')} (ID: {galardon.get('id', 'N/A')})")
                    return galardones_obtenidos
                
                # Verificar galardones específicos
                galardon_ids_obtenidos = [g.get('galardon_id', g.get('id')) for g in galardones_obtenidos]
                galardones_faltantes = [g for g in galardones_esperados if g not in galardon_ids_obtenidos]
                
                if not galardones_faltantes:
                    self.print_success(f"Usuario tiene todos los galardones esperados: {len(galardones_obtenidos)} galardones")
                    for galardon in galardones_obtenidos:
                        print(f"   - {galardon.get('nombre', 'Sin nombre')} (ID: {galardon.get('id', 'N/A')})")
                    return galardones_obtenidos
                else:
                    self.print_error(f"Faltan galardones: {galardones_faltantes}")
                    print(f"   Galardones obtenidos: {galardon_ids_obtenidos}")
                    return galardones_obtenidos
            else:
                self.print_error(f"Error obteniendo galardones de usuario: {resp.status_code} - {resp.text}")
                return None
                
        except Exception as e:
            self.print_error(f"Error verificando galardones de usuario: {e}")
            return None

    def test_flujo_completo_galardon_usuario(self):
        """Prueba completa: crear usuario, crear galardón, asignar y verificar"""
        self.print_test_header("FLUJO COMPLETO: ASIGNACIÓN Y VERIFICACIÓN DE GALARDÓN")
        
        # Paso 1: Crear usuario de prueba
        self.print_info("Paso 1: Creando usuario de prueba...")
        usuario_id = self.crear_usuario_prueba("_flujo_completo")
        if not usuario_id:
            self.print_error("No se pudo crear usuario. Abortando prueba.")
            return False
        
        self.wait_for_operation()
        
        # Paso 2: Crear galardón de prueba
        self.print_info("Paso 2: Creando galardón de prueba...")
        galardon_id = self.test_crear_galardon(
            "Galardón de Prueba Flujo Completo", 
            "Galardón creado para probar el flujo completo de asignación",
            "flujo_completo.jpg",
            "prueba"
        )
        if not galardon_id:
            self.print_error("No se pudo crear galardón. Abortando prueba.")
            return False
        
        self.wait_for_operation()
        
        # Paso 3: Verificar que el usuario no tiene galardones inicialmente
        self.print_info("Paso 3: Verificando estado inicial (sin galardones)...")
        galardones_iniciales = self.test_verificar_galardones_usuario(usuario_id, [])
        if galardones_iniciales and len(galardones_iniciales) > 0:
            self.print_error("El usuario ya tenía galardones inicialmente")
            return False
        
        self.wait_for_operation()
        
        # Paso 4: Asignar galardón al usuario
        self.print_info("Paso 4: Asignando galardón al usuario...")
        asignacion_id = self.test_asignar_galardon_a_usuario(usuario_id, galardon_id)
        if not asignacion_id:
            self.print_error("No se pudo asignar el galardón al usuario")
            return False
        
        self.wait_for_operation()
        
        # Paso 5: Verificar que el usuario recibió el galardón
        self.print_info("Paso 5: Verificando que el usuario recibió el galardón...")
        galardones_finales = self.test_verificar_galardones_usuario(usuario_id, [galardon_id])
        if not galardones_finales or len(galardones_finales) == 0:
            self.print_error("El usuario no recibió el galardón asignado")
            return False
        
        self.print_success("✅ FLUJO COMPLETO EXITOSO: Usuario creó, asignó y recibió galardón correctamente")
        return True

    def test_asignacion_multiple_galardones(self):
        """Prueba asignar múltiples galardones a un usuario y verificar"""
        self.print_test_header("PRUEBA: ASIGNACIÓN MÚLTIPLE DE GALARDONES")
        
        # Crear usuario
        usuario_id = self.crear_usuario_prueba("_multiple")
        if not usuario_id:
            return False
        
        self.wait_for_operation()
        
        # Crear múltiples galardones
        galardon_ids = []
        galardon_nombres = ["Galardón Bronce", "Galardón Plata", "Galardón Oro"]
        
        for nombre in galardon_nombres:
            galardon_id = self.test_crear_galardon(
                nombre,
                f"Descripción de {nombre}",
                f"{nombre.lower().replace(' ', '_')}.jpg",
                "nivel"
            )
            if galardon_id:
                galardon_ids.append(galardon_id)
            self.wait_for_operation()
        
        if len(galardon_ids) < 3:
            self.print_error("No se pudieron crear todos los galardones de prueba")
            return False
        
        # Asignar todos los galardones al usuario
        for galardon_id in galardon_ids:
            self.test_asignar_galardon_a_usuario(usuario_id, galardon_id)
            self.wait_for_operation()
        
        # Verificar que el usuario tiene todos los galardones
        galardones_obtenidos = self.test_verificar_galardones_usuario(usuario_id, galardon_ids)
        
        if galardones_obtenidos and len(galardones_obtenidos) == len(galardon_ids):
            self.print_success(f"✅ ASIGNACIÓN MÚLTIPLE EXITOSA: Usuario recibió {len(galardon_ids)} galardones")
            return True
        else:
            self.print_error(f"Asignación múltiple falló: esperados {len(galardon_ids)}, obtenidos {len(galardones_obtenidos) if galardones_obtenidos else 0}")
            return False

    # --- MÉTODOS EXISTENTES (mantenidos del código original) ---
    
    def test_crear_galardon(self, nombre, descripcion, imagen_url, tipo, expected_success=True):
        """Prueba para crear galardón"""
        galardon_data = {
            "nombre": nombre,
            "descripcion": descripcion,
            "imagen_url": imagen_url,
            "tipo": tipo
        }
        
        try:
            resp = requests.post(f"{BASE_URL}/galardones/", json=galardon_data)
            
            if expected_success and resp.status_code == 201:
                galardon_id = resp.json()['id']
                self.created_ids['galardones'].append(galardon_id)
                self.print_success(f"Galardón creado: {nombre} (ID: {galardon_id})")
                return galardon_id
            elif not expected_success and resp.status_code != 201:
                self.print_success(f"Creación fallida como se esperaba: {resp.status_code}")
                return None
            else:
                self.print_error(f"Resultado inesperado. {resp.status_code} - {resp.text}")
                return None
                
        except Exception as e:
            self.print_error(f"Error creando galardón: {e}")
            return None

    def test_obtener_galardon_por_id(self, galardon_id, expected_success=True):
        """Prueba obtener galardón por ID"""
        self.print_test_header(f"OBTENER GALARDÓN POR ID: {galardon_id}")
        
        try:
            resp = requests.get(f"{BASE_URL}/galardones/{galardon_id}/")
            
            if expected_success and resp.status_code == 200:
                detalle = resp.json()
                self.print_success(f"Galardón obtenido: {detalle['nombre']}")
                return detalle
            elif not expected_success and resp.status_code == 404:
                self.print_success("Galardón no encontrado (como se esperaba)")
                return None
            else:
                self.print_error(f"Resultado inesperado. {resp.status_code} - {resp.text}")
                return None
                
        except Exception as e:
            self.print_error(f"Error obteniendo galardón: {e}")
            return None

    def test_obtener_todos_galardones(self, expected_min_count=0):
        """Prueba obtener todos los galardones"""
        self.print_test_header("OBTENER TODOS LOS GALARDONES")
        
        try:
            resp = requests.get(f"{BASE_URL}/galardones/")
            
            if resp.status_code == 200:
                galardones = resp.json()
                if len(galardones) >= expected_min_count:
                    self.print_success(f"Obtenidos {len(galardones)} galardones")
                    return galardones
                else:
                    self.print_error(f"Se esperaban al menos {expected_min_count} galardones, se obtuvieron {len(galardones)}")
                    return galardones
            else:
                self.print_error(f"Error obteniendo galardones. Código: {resp.status_code}")
                return None
                
        except Exception as e:
            self.print_error(f"Error obteniendo galardones: {e}")
            return None

    def test_actualizar_galardon(self, galardon_id, nuevos_datos, expected_success=True):
        """Prueba actualizar galardón"""
        self.print_test_header(f"ACTUALIZAR GALARDÓN: {galardon_id}")
        
        try:
            resp = requests.put(f"{BASE_URL}/galardones/{galardon_id}/", json=nuevos_datos)
            
            if expected_success and resp.status_code == 200:
                galardon_actualizado = resp.json()
                self.print_success(f"Galardón actualizado: {galardon_actualizado['nombre']}")
                return galardon_actualizado
            elif not expected_success and resp.status_code != 200:
                self.print_success("Actualización fallida como se esperaba")
                return None
            else:
                self.print_error(f"Resultado inesperado. {resp.status_code} - {resp.text}")
                return None
                
        except Exception as e:
            self.print_error(f"Error actualizando galardón: {e}")
            return None

    def test_eliminar_galardon(self, galardon_id, expected_success=True):
        """Prueba eliminar galardón"""
        self.print_test_header(f"ELIMINAR GALARDÓN: {galardon_id}")
        
        try:
            resp = requests.delete(f"{BASE_URL}/galardones/{galardon_id}")
            
            if expected_success and resp.status_code == 200:
                self.print_success(f"Galardón {galardon_id} eliminado exitosamente")
                if galardon_id in self.created_ids['galardones']:
                    self.created_ids['galardones'].remove(galardon_id)
                return True
            elif not expected_success and resp.status_code == 404:
                self.print_success("Eliminación fallida como se esperaba (galardón no existe)")
                return False
            else:
                self.print_error(f"Resultado inesperado.{resp.status_code} - {resp.text}")
                return False
                
        except Exception as e:
            self.print_error(f"Error eliminando galardón: {e}")
            return False

    def test_obtener_galardones_usuario(self, usuario_id, expected_empty=False):
        """Prueba obtener galardones de usuario"""
        self.print_test_header(f"OBTENER GALARDONES DE USUARIO: {usuario_id}")
        
        try:
            resp = requests.get(f"{BASE_URL}/usuarios/{usuario_id}/galardones")
            
            if resp.status_code == 200:
                galardones_usuario = resp.json()
                if expected_empty and len(galardones_usuario) == 0:
                    self.print_success("Usuario sin galardones (como se esperaba)")
                elif not expected_empty and len(galardones_usuario) > 0:
                    self.print_success(f"Obtenidos {len(galardones_usuario)} galardones del usuario")
                else:
                    self.print_success(f"Obtenidos {len(galardones_usuario)} galardones del usuario")
                return galardones_usuario
            else:
                self.print_error(f"Error obteniendo galardones de usuario. {resp.status_code} - {resp.text}")
                return None
                
        except Exception as e:
            self.print_error(f"Error obteniendo galardones de usuario: {e}")
            return None

    def test_paginacion_galardones(self, skip=0, limit=2):
        """Prueba paginación de galardones"""
        self.print_test_header(f"PAGINACIÓN DE GALARDONES (skip={skip}, limit={limit})")
        
        try:
            resp = requests.get(f"{BASE_URL}/galardones/", params={"skip": skip, "limit": limit})
            
            if resp.status_code == 200:
                galardones_paginados = resp.json()
                if len(galardones_paginados) <= limit:
                    self.print_success(f"Paginación OK: {len(galardones_paginados)} galardones")
                    return galardones_paginados
                else:
                    self.print_error(f"Paginación falló: se obtuvieron {len(galardones_paginados)} galardones (límite: {limit})")
                    return galardones_paginados
            else:
                self.print_error(f"Error en paginación. {resp.status_code} - {resp.text}")
                return None
                
        except Exception as e:
            self.print_error(f"Error en paginación: {e}")
            return None

    def test_crear_galardon_duplicado(self, galardon_data):
        """Prueba crear galardón duplicado"""
        self.print_test_header("CREAR GALARDÓN DUPLICADO")
        
        try:
            resp = requests.post(f"{BASE_URL}/galardones/", json=galardon_data)
            
            if resp.status_code == 409:
                self.print_success("Error 409 recibido correctamente (conflicto de duplicados)")
                return True
            else:
                self.print_error(f"Se esperaba 409 pero se recibió {resp.status_code}")
                return False
                
        except Exception as e:
            self.print_error(f"Error creando galardón duplicado: {e}")
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

    def run_comprehensive_test(self):
        """Ejecuta una prueba completa de todos los endpoints de galardones"""
        self.print_test_header("INICIANDO PRUEBA COMPREHENSIVA DE GALARDONES")
        
        # Paso 0: Verificar servidor
        self.print_info("Paso 0: Verificando conexión al servidor...")
        if not self.test_servidor_conectado():
            return
        
        # Paso 1: Probar flujo completo de asignación
        self.print_info("Paso 1: Probando flujo completo de asignación de galardón...")
        self.test_flujo_completo_galardon_usuario()
        self.wait_for_operation(1)
        
        # Paso 2: Probar asignación múltiple
        self.print_info("Paso 2: Probando asignación múltiple de galardones...")
        self.test_asignacion_multiple_galardones()
        self.wait_for_operation(1)
        
        # Paso 3: Crear galardones de prueba adicionales
        self.print_info("Paso 3: Creando galardones de prueba adicionales...")
        
        galardon1_id = self.test_crear_galardon(
            "Catador Inicial", 
            "Galardón por probar cervezas diferentes",
            "catador_inicial.jpg",
            "cantidad"
        )
        self.wait_for_operation()
        
        galardon2_id = self.test_crear_galardon(
            "Viajero Cervecero",
            "Galardón por probar cervezas de diferentes países",
            "viajero_cervecero.jpg", 
            "variedad"
        )
        self.wait_for_operation()
        
        if not all([galardon1_id, galardon2_id]):
            self.print_error("No se pudieron crear galardones adicionales")
        
        # Paso 4: Probar obtención de galardones
        self.print_info("Paso 4: Probando obtención de galardones...")
        if galardon1_id:
            self.test_obtener_galardon_por_id(galardon1_id)
            self.wait_for_operation()
        
        self.test_obtener_todos_galardones(expected_min_count=2)
        self.wait_for_operation()
        
        # Paso 5: Probar actualización de galardones
        self.print_info("Paso 5: Probando actualización de galardones...")
        if galardon1_id:
            self.test_actualizar_galardon(
                galardon1_id,
                {
                    "nombre": "Catador Inicial Actualizado",
                    "descripcion": "Descripción actualizada del galardón catador",
                    "tipo": "cantidad"
                }
            )
            self.wait_for_operation()
        
        # Paso 6: Probar casos de error
        self.print_info("Paso 6: Probando casos de error...")
        self.test_obtener_galardon_por_id(9999, expected_success=False)  # Galardón inexistente
        self.wait_for_operation()
        
        # Paso 7: Probar paginación
        self.print_info("Paso 7: Probando paginación...")
        self.test_paginacion_galardones(skip=0, limit=2)
        self.wait_for_operation()
        
        # Paso 8: Probar eliminación
        self.print_info("Paso 8: Probando eliminación de galardones...")
        if self.created_ids['galardones']:
            galardon_a_eliminar = self.created_ids['galardones'][0]
            self.test_eliminar_galardon(galardon_a_eliminar)
            self.wait_for_operation()
        
        # Resultados finales
        self.print_test_summary()

    def run_quick_test(self):
        """Ejecuta una prueba rápida con datos existentes"""
        self.print_test_header("INICIANDO PRUEBA RÁPIDA DE GALARDONES")
        
        # Verificar servidor
        if not self.test_servidor_conectado():
            return
        
        # Probar endpoints básicos con datos existentes
        self.test_obtener_todos_galardones()
        self.wait_for_operation()
        
        # Si hay galardones, probar obtener uno específico
        galardones = self.test_obtener_todos_galardones()
        if galardones and len(galardones) > 0:
            primer_galardon_id = galardones[0]['id']
            self.test_obtener_galardon_por_id(primer_galardon_id)
            self.wait_for_operation()
        
        # Probar paginación
        self.test_paginacion_galardones(limit=1)
        
        self.print_test_summary()

    def print_test_summary(self):
        """Imprime un resumen de los resultados de las pruebas"""
        self.print_test_header("RESUMEN DE PRUEBAS DE GALARDONES")
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
            print("\n🎉 ¡TODAS LAS PRUEBAS DE GALARDONES EXITOSAS!")
        elif self.test_results['passed'] > 0:
            print("\n⚠️  Algunas pruebas fallaron, pero otras fueron exitosas")
        else:
            print("\n💥 Todas las pruebas fallaron")

# --- Ejecución de pruebas ---
if __name__ == "__main__":
    tester = GalardonTester()
    
    print("Iniciando pruebas de API de Galardones...")
    print("Asegúrate de que el servidor Flask esté ejecutándose en http://localhost:8000")
    time.sleep(2)
    
    # Ejecutar prueba comprehensiva (crea y elimina datos de prueba)
    tester.run_comprehensive_test()
    
    # O ejecutar prueba rápida (usa datos existentes)
    # tester.run_quick_test()
    
    # Limpieza final
    tester.cleanup()