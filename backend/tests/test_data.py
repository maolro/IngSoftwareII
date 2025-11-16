import requests
import json
import time
import random

# --- Configuración ---
BASE_URL = "http://localhost:8000/api"

class DatabaseSeeder:
    """Clase para poblar la base de datos con datos de prueba para la demo"""
    
    def __init__(self):
        self.created_ids = {
            'usuarios': [],
            'cervezas': [],
            'cervecerias': [],
            'degustaciones': [],
            'galardones': [],
            'comentarios': []
        }
        self.stats = {
            'created': 0,
            'errors': 0
        }
    
    def print_header(self, message):
        """Imprime un cabezal bonito"""
        print("\n" + "="*70)
        print(f" 🎯 {message}")
        print("="*70)
    
    def print_success(self, message):
        """Print success message"""
        print(f"✅ {message}")
        self.stats['created'] += 1
    
    def print_error(self, message, error=None):
        """Print error message"""
        print(f"❌ {message}")
        if error:
            print(f"   Error: {error}")
        self.stats['errors'] += 1
    
    def print_info(self, message):
        """Print info message"""
        print(f"\nℹ️  {message}")
    
    def wait_for_operation(self, seconds=0.3):
        """Wait between operations"""
        time.sleep(seconds)
    
    def test_servidor_conectado(self):
        """Verifica que el servidor esté conectado"""
        self.print_header("VERIFICANDO CONEXIÓN AL SERVIDOR")
        
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

    # --- Funciones para crear datos ---

    def crear_usuarios(self):
        """Crea usuarios de prueba"""
        self.print_header("CREANDO USUARIOS DE PRUEBA")
        
        usuarios_data = [
            {
                "username": "alex_cervecero",
                "email": "alex@beersp.com",
                "password": "password123",
                "birth_date": "1990-05-15"
            },
            {
                "username": "maria_catadora", 
                "email": "maria@beersp.com",
                "password": "password123",
                "birth_date": "1992-08-22"
            },
            {
                "username": "carlos_brewmaster",
                "email": "carlos@beersp.com", 
                "password": "password123",
                "birth_date": "1988-03-10"
            },
            {
                "username": "laura_hoplover",
                "email": "laura@beersp.com",
                "password": "password123", 
                "birth_date": "1995-11-30"
            },
            {
                "username": "david_ipaexpert",
                "email": "david@beersp.com",
                "password": "password123",
                "birth_date": "1991-07-08"
            }
        ]
        
        usuarios_creados = []
        for user_data in usuarios_data:
            try:
                resp = requests.post(f"{BASE_URL}/usuarios/", json=user_data)
                if resp.status_code == 201:
                    usuario_id = resp.json()['id']
                    self.created_ids['usuarios'].append(usuario_id)
                    usuarios_creados.append(usuario_id)
                    self.print_success(f"Usuario creado: {user_data['username']} (ID: {usuario_id})")
                else:
                    self.print_error(f"Error creando usuario {user_data['username']}: {resp.status_code} - {resp.text}")
            except Exception as e:
                self.print_error(f"Error creando usuario {user_data['username']}: {e}")
            
            self.wait_for_operation()
        
        return usuarios_creados

    def crear_amistades(self, usuarios_ids):
        """Crea relaciones de amistad entre usuarios"""
        self.print_header("CREANDO RELACIONES DE AMISTAD")
        
        if len(usuarios_ids) < 3:
            self.print_error("No hay suficientes usuarios para crear amistades")
            return
        
        # Alex es amigo de María y Carlos
        self.crear_amistad(usuarios_ids[0], usuarios_ids[1])
        self.crear_amistad(usuarios_ids[0], usuarios_ids[2])
        
        # María es amiga de Laura
        self.crear_amistad(usuarios_ids[1], usuarios_ids[3])
        
        # Carlos es amigo de David
        self.crear_amistad(usuarios_ids[2], usuarios_ids[4])
        
        # Laura es amiga de David
        self.crear_amistad(usuarios_ids[3], usuarios_ids[4])
    
    def crear_amistad(self, usuario_id, amigo_id):
        """Crea una relación de amistad individual"""
        try:
            amigo_data = {"friend_id": amigo_id}
            resp = requests.post(f"{BASE_URL}/usuarios/{usuario_id}/amigos/", json=amigo_data)
            
            if resp.status_code == 201:
                self.print_success(f"Amistad creada: {usuario_id} -> {amigo_id}")
            else:
                self.print_error(f"Error creando amistad {usuario_id} -> {amigo_id}: {resp.status_code}")
        except Exception as e:
            self.print_error(f"Error creando amistad: {e}")

    def crear_cervezas(self):
        """Crea cervezas de prueba"""
        self.print_header("CREANDO CERVEZAS DE PRUEBA")
        
        cervezas_data = [
            {
                "nombre": "Mahou Cinco Estrellas",
                "descripcion": "Cerveza lager española clásica, suave y refrescante",
                "foto": "mahou_cinco.jpg",
                "estilo": "Lager",
                "pais_procedencia": "España",
                "tamano": "330ml",
                "formato": "Botella", 
                "porcentaje_alcohol": 5.5,
                "ibu": 18,
                "color": "Dorado"
            },
            {
                "nombre": "Estrella Galicia",
                "descripcion": "Cerveza gallega con carácter, ligeramente amarga",
                "foto": "estrella_galicia.jpg", 
                "estilo": "Pilsen",
                "pais_procedencia": "España",
                "tamano": "330ml",
                "formato": "Latina",
                "porcentaje_alcohol": 5.5,
                "ibu": 22,
                "color": "Dorado pálido"
            },
            {
                "nombre": "Alhambra Reserva 1925", 
                "descripcion": "Cerveza de fermentación baja, suave y aromática",
                "foto": "alhambra_1925.jpg",
                "estilo": "Lager",
                "pais_procedencia": "España",
                "tamano": "330ml",
                "formato": "Botella",
                "porcentaje_alcohol": 6.4,
                "ibu": 23,
                "color": "Ámbar"
            },
            {
                "nombre": "IPA Citra",
                "descripcion": "India Pale Ale con notas cítricas y afrutadas",
                "foto": "ipa_citra.jpg",
                "estilo": "IPA",
                "pais_procedencia": "EEUU",
                "tamano": "440ml", 
                "formato": "Lata",
                "porcentaje_alcohol": 6.8,
                "ibu": 65,
                "color": "Ámbar dorado"
            },
            {
                "nombre": "Guinness Draught",
                "descripcion": "Stout irlandesa cremosa con sabor a café y chocolate",
                "foto": "guinness.jpg",
                "estilo": "Stout", 
                "pais_procedencia": "Irlanda",
                "tamano": "500ml",
                "formato": "Barril",
                "porcentaje_alcohol": 4.2,
                "ibu": 45,
                "color": "Negro"
            },
            {
                "nombre": "Weihenstephaner Hefeweissbier",
                "descripcion": "Cerveza de trigo alemana con notas de plátano y clavo",
                "foto": "weihenstephaner.jpg",
                "estilo": "Weissbier",
                "pais_procedencia": "Alemania",
                "tamano": "500ml",
                "formato": "Botella",
                "porcentaje_alcohol": 5.4,
                "ibu": 14,
                "color": "Turba"
            }
        ]
        
        cervezas_creadas = []
        for cerveza_data in cervezas_data:
            try:
                resp = requests.post(f"{BASE_URL}/cervezas/", json=cerveza_data)
                if resp.status_code == 201:
                    cerveza_id = resp.json()['id']
                    self.created_ids['cervezas'].append(cerveza_id)
                    cervezas_creadas.append(cerveza_id)
                    self.print_success(f"Cerveza creada: {cerveza_data['nombre']} (ID: {cerveza_id})")
                else:
                    self.print_error(f"Error creando cerveza {cerveza_data['nombre']}: {resp.status_code} - {resp.text}")
            except Exception as e:
                self.print_error(f"Error creando cerveza {cerveza_data['nombre']}: {e}")
            
            self.wait_for_operation()
        
        return cervezas_creadas

    def crear_cervecerias(self):
        """Crea cervecerías de prueba"""
        self.print_header("CREANDO CERVECERÍAS DE PRUEBA")
        
        cervecerias_data = [
            {
                "nombre": "Cervecería La Tradición",
                "direccion": "Calle Mayor 123, Madrid",
                "ciudad": "Madrid",
                "pais": "España", 
                "descripcion": "Cervecería tradicional con las mejores cervezas españolas",
                "telefono": "+34 91 123 4567",
                "horario": "L-D: 12:00-02:00",
                "foto": "tradicion.jpg"
            },
            {
                "nombre": "Brew & Blues",
                "direccion": "Avenida Libertad 45, Barcelona", 
                "ciudad": "Barcelona",
                "pais": "España",
                "descripcion": "Cervecería moderna con música en vivo y cervezas artesanales",
                "telefono": "+34 93 987 6543",
                "horario": "L-V: 18:00-02:00, S-D: 12:00-03:00",
                "foto": "brew_blues.jpg"
            },
            {
                "nombre": "Hoppy Corner",
                "direccion": "Plaza Central 67, Valencia",
                "ciudad": "Valencia", 
                "pais": "España",
                "descripcion": "Especialistas en IPAs y cervezas con alto lúpulo",
                "telefono": "+34 96 555 4444",
                "horario": "M-D: 17:00-01:00",
                "foto": "hoppy_corner.jpg"
            },
            {
                "nombre": "The Irish Pub",
                "direccion": "Calle Irlanda 89, Madrid",
                "ciudad": "Madrid",
                "pais": "España", 
                "descripcion": "Auténtico pub irlandés con Guinness de barril",
                "telefono": "+34 91 888 9999",
                "horario": "L-D: 11:00-03:00",
                "foto": "irish_pub.jpg"
            }
        ]
        
        cervecerias_creadas = []
        for cerveceria_data in cervecerias_data:
            try:
                resp = requests.post(f"{BASE_URL}/cervecerias/", json=cerveceria_data)
                if resp.status_code == 201:
                    cerveceria_id = resp.json()['id']
                    self.created_ids['cervecerias'].append(cerveceria_id)
                    cervecerias_creadas.append(cerveceria_id)
                    self.print_success(f"Cervecería creada: {cerveceria_data['nombre']} (ID: {cerveceria_id})")
                else:
                    self.print_error(f"Error creando cervecería {cerveceria_data['nombre']}: {resp.status_code} - {resp.text}")
            except Exception as e:
                self.print_error(f"Error creando cervecería {cerveceria_data['nombre']}: {e}")
            
            self.wait_for_operation()
        
        return cervecerias_creadas

    def crear_degustaciones(self, usuarios_ids, cervezas_ids, cervecerias_ids):
        """Crea degustaciones de prueba"""
        self.print_header("CREANDO DEGUSTACIONES DE PRUEBA")
        
        degustaciones_data = []
        
        # Alex prueba varias cervezas
        degustaciones_data.extend([
            {"usuario_id": usuarios_ids[0], "cerveza_id": cervezas_ids[0], "cerveceria_id": cervecerias_ids[0], "puntuacion": 4.0, "comentario": "Muy refrescante, perfecta para el verano"},
            {"usuario_id": usuarios_ids[0], "cerveza_id": cervezas_ids[3], "cerveceria_id": cervecerias_ids[1], "puntuacion": 4.5, "comentario": "Excelente IPA, muy aromática"},
            {"usuario_id": usuarios_ids[0], "cerveza_id": cervezas_ids[4], "cerveceria_id": cervecerias_ids[3], "puntuacion": 3.5, "comentario": "Auténtica Guinness, pero un poco pesada"}
        ])
        
        # María prueba cervezas
        degustaciones_data.extend([
            {"usuario_id": usuarios_ids[1], "cerveza_id": cervezas_ids[1], "cerveceria_id": cervecerias_ids[0], "puntuacion": 4.2, "comentario": "Me encanta el carácter gallego de esta cerveza"},
            {"usuario_id": usuarios_ids[1], "cerveza_id": cervezas_ids[5], "cerveceria_id": cervecerias_ids[2], "puntuacion": 4.8, "comentario": "Increíble cerveza de trigo, las mejores notas"}
        ])
        
        # Carlos prueba cervezas
        degustaciones_data.extend([
            {"usuario_id": usuarios_ids[2], "cerveza_id": cervezas_ids[2], "cerveceria_id": cervecerias_ids[1], "puntuacion": 4.3, "comentario": "Alhambra siempre fiel a su calidad"},
            {"usuario_id": usuarios_ids[2], "cerveza_id": cervezas_ids[3], "puntuacion": 4.7, "comentario": "Una de las mejores IPAs que he probado"}
        ])
        
        # Laura y David también prueban
        degustaciones_data.extend([
            {"usuario_id": usuarios_ids[3], "cerveza_id": cervezas_ids[4], "cerveceria_id": cervecerias_ids[3], "puntuacion": 4.0, "comentario": "Perfecta crema y sabor"},
            {"usuario_id": usuarios_ids[4], "cerveza_id": cervezas_ids[0], "puntuacion": 3.8, "comentario": "Buena lager tradicional"}
        ])
        
        degustaciones_creadas = []
        for degustacion_data in degustaciones_data:
            try:
                resp = requests.post(f"{BASE_URL}/degustaciones/", json=degustacion_data)
                if resp.status_code == 201:
                    degustacion_id = resp.json()['id']
                    self.created_ids['degustaciones'].append(degustacion_id)
                    degustaciones_creadas.append(degustacion_id)
                    self.print_success(f"Degustación creada (Usuario: {degustacion_data['usuario_id']}, Cerveza: {degustacion_data['cerveza_id']})")
                else:
                    self.print_error(f"Error creando degustación: {resp.status_code} - {resp.text}")
            except Exception as e:
                self.print_error(f"Error creando degustación: {e}")
            
            self.wait_for_operation(0.2)
        
        return degustaciones_creadas

    def crear_galardones(self, usuarios_ids):
        """Crea galardones de prueba"""
        self.print_header("CREANDO GALARDONES DE PRUEBA")
        
        galardones_data = [
            {
                "nombre": "Catador Inicial",
                "descripcion": "Galardón por probar tus primeras cervezas",
                "imagen_url": "catador_inicial.png",
                "tipo": "cantidad",
                "condiciones": {"cervezas_minimas": 3}
            },
            {
                "nombre": "Viajero Cervecero", 
                "descripcion": "Galardón por probar cervezas de diferentes países",
                "imagen_url": "viajero_cervecero.png",
                "tipo": "variedad",
                "condiciones": {"paises_minimos": 2}
            },
            {
                "nombre": "Maestro de IPA",
                "descripcion": "Galardón por dominar las India Pale Ales",
                "imagen_url": "maestro_ipa.png", 
                "tipo": "estilo",
                "condiciones": {"ipas_minimas": 2}
            }
        ]
        
        galardones_creados = []
        for galardon_data in galardones_data:
            try:
                resp = requests.post(f"{BASE_URL}/galardones/", json=galardon_data)
                if resp.status_code == 201:
                    galardon_id = resp.json()['id']
                    self.created_ids['galardones'].append(galardon_id)
                    galardones_creados.append(galardon_id)
                    self.print_success(f"Galardón creado: {galardon_data['nombre']} (ID: {galardon_id})")
                else:
                    self.print_error(f"Error creando galardón {galardon_data['nombre']}: {resp.status_code} - {resp.text}")
            except Exception as e:
                self.print_error(f"Error creando galardón {galardon_data['nombre']}: {e}")
            
            self.wait_for_operation()
        
        # Asignar algunos galardones a usuarios
        if galardones_creados and usuarios_ids:
            self.asignar_galardones_a_usuarios(usuarios_ids, galardones_creados)
        
        return galardones_creados

    def asignar_galardones_a_usuarios(self, usuarios_ids, galardones_ids):
        """Asigna galardones a usuarios"""
        self.print_info("Asignando galardones a usuarios...")
        
        # Alex obtiene el galardón de Catador Inicial
        self.asignar_galardon_usuario(usuarios_ids[0], galardones_ids[0], 1, 3)
        
        # María obtiene el galardón de Viajero Cervecero  
        self.asignar_galardon_usuario(usuarios_ids[1], galardones_ids[1], 1, 2)
        
        # Carlos obtiene el galardón de Maestro de IPA
        self.asignar_galardon_usuario(usuarios_ids[2], galardones_ids[2], 1, 2)

    def asignar_galardon_usuario(self, usuario_id, galardon_id, nivel=1, progreso=0):
        """Asigna un galardón específico a un usuario"""
        try:
            asignacion_data = {
                "galardon_id": galardon_id,
                "nivel_actual": nivel,
                "progreso_actual": progreso
            }
            resp = requests.post(f"{BASE_URL}/usuarios/{usuario_id}/galardones", json=asignacion_data)
            if resp.status_code == 201:
                self.print_success(f"Galardón {galardon_id} asignado a usuario {usuario_id}")
            else:
                self.print_error(f"Error asignando galardón: {resp.status_code} - {resp.text}")
        except Exception as e:
            self.print_error(f"Error asignando galardón: {e}")

    def crear_comentarios(self, degustaciones_ids, usuarios_ids):
        """Crea comentarios en degustaciones"""
        self.print_header("CREANDO COMENTARIOS EN DEGUSTACIONES")
        
        if not degustaciones_ids or len(degustaciones_ids) < 2:
            self.print_error("No hay suficientes degustaciones para comentar")
            return
        
        comentarios_data = [
            {
                "degustacion_id": degustaciones_ids[0],
                "usuario_id": usuarios_ids[1],
                "comentario": "¡Totalmente de acuerdo! Mahou es perfecta para el calor"
            },
            {
                "degustacion_id": degustaciones_ids[1], 
                "usuario_id": usuarios_ids[2],
                "comentario": "Esa IPA es mi favorita también, gran elección"
            },
            {
                "degustacion_id": degustaciones_ids[3],
                "usuario_id": usuarios_ids[0], 
                "comentario": "Estrella Galicia nunca falla, buena elección María"
            }
        ]
        
        for comentario_data in comentarios_data:
            try:
                resp = requests.post(f"{BASE_URL}/degustaciones/{comentario_data['degustacion_id']}/comentarios/", json=comentario_data)
                if resp.status_code == 201:
                    comentario_id = resp.json()['id']
                    self.created_ids['comentarios'].append(comentario_id)
                    self.print_success(f"Comentario creado en degustación {comentario_data['degustacion_id']}")
                else:
                    self.print_error(f"Error creando comentario: {resp.status_code} - {resp.text}")
            except Exception as e:
                self.print_error(f"Error creando comentario: {e}")
            
            self.wait_for_operation(0.2)

    # --- Función principal para poblar la base de datos ---

    def poblar_base_datos(self):
        """Función principal que pobla toda la base de datos"""
        self.print_header("INICIANDO POBLADO DE BASE DE DATOS PARA DEMO")
        
        # Verificar servidor
        if not self.test_servidor_conectado():
            return False
        
        # Crear datos en orden
        usuarios_ids = self.crear_usuarios()
        self.wait_for_operation(1)
        
        if usuarios_ids:
            self.crear_amistades(usuarios_ids)
            self.wait_for_operation(1)
        
        cervezas_ids = self.crear_cervezas()
        self.wait_for_operation(1)
        
        cervecerias_ids = self.crear_cervecerias()
        self.wait_for_operation(1)
        
        if usuarios_ids and cervezas_ids:
            degustaciones_ids = self.crear_degustaciones(usuarios_ids, cervezas_ids, cervecerias_ids)
            self.wait_for_operation(1)
            
            if degustaciones_ids:
                self.crear_comentarios(degustaciones_ids, usuarios_ids)
                self.wait_for_operation(1)
        
        if usuarios_ids:
            self.crear_galardones(usuarios_ids)
        
        # Mostrar resumen
        self.mostrar_resumen()
        return True

    # --- Función para limpiar la base de datos ---

    def limpiar_base_datos(self):
        """Limpia todos los datos de la base de datos"""
        self.print_header("LIMPIANDO BASE DE DATOS COMPLETA")
        
        if not self.test_servidor_conectado():
            return False
        
        total_eliminados = 0
        
        # Limpiar en orden inverso para respetar foreign keys
        categorias = ['degustaciones', 'usuarios', 'cervezas', 'cervecerias', 'galardones']
        
        for categoria in categorias:
            if categoria in self.created_ids and self.created_ids[categoria]:
                print(f"\nEliminando {categoria}...")
                for item_id in self.created_ids[categoria][:]:
                    try:
                        if categoria == 'usuarios':
                            resp = requests.delete(f"{BASE_URL}/usuarios/{item_id}")
                        elif categoria == 'cervezas':
                            resp = requests.delete(f"{BASE_URL}/cervezas/{item_id}")
                        elif categoria == 'cervecerias':
                            resp = requests.delete(f"{BASE_URL}/cervecerias/{item_id}")
                        elif categoria == 'galardones':
                            resp = requests.delete(f"{BASE_URL}/galardones/{item_id}")
                        # Los comentarios y degustaciones se eliminan automáticamente por CASCADE
                        
                        if resp.status_code in [200, 204]:
                            self.created_ids[categoria].remove(item_id)
                            total_eliminados += 1
                            print(f"  ✅ {categoria[:-1]} {item_id} eliminado")
                        else:
                            print(f"  ⚠️  No se pudo eliminar {categoria} {item_id}: {resp.status_code}")
                    except Exception as e:
                        print(f"  ❌ Error eliminando {categoria} {item_id}: {e}")
                    
                    self.wait_for_operation(0.1)
        
        print(f"\n🧹 Limpieza completada: {total_eliminados} elementos eliminados")
        return True

    def limpiar_todo_por_api(self):
        """Limpia TODOS los datos de la base de datos mediante la API"""
        self.print_header("LIMPIANDO TODA LA BASE DE DATOS (MODO NUCLEAR)")
        
        if not self.test_servidor_conectado():
            return False
        
        # Obtener todos los elementos existentes y eliminarlos
        categorias = [
            ('comentarios', f"{BASE_URL}/comentarios/"),
            ('degustaciones', f"{BASE_URL}/degustaciones/"),
            ('galardones', f"{BASE_URL}/galardones/"),
            ('usuarios', f"{BASE_URL}/usuarios/"),
            ('cervezas', f"{BASE_URL}/cervezas/"),
            ('cervecerias', f"{BASE_URL}/cervecerias/")
        ]
        
        total_eliminados = 0
        
        for categoria, url in categorias:
            try:
                # Obtener todos los elementos
                resp = requests.get(url)
                if resp.status_code == 200:
                    elementos = resp.json()
                    print(f"\nEliminando {len(elementos)} {categoria}...")
                    
                    for elemento in elementos:
                        try:
                            delete_url = f"{url.rstrip('/')}/{elemento['id']}"
                            delete_resp = requests.delete(delete_url)
                            
                            if delete_resp.status_code in [200, 204]:
                                total_eliminados += 1
                                print(f"  ✅ {categoria[:-1]} {elemento['id']} eliminado")
                            else:
                                error_msg = delete_resp.json().get('error', 'Error desconocido')
                                print(f"  ⚠️  No se pudo eliminar {categoria} {elemento['id']}: {error_msg}")
                        except Exception as e:
                            print(f"  ❌ Error eliminando {categoria} {elemento['id']}: {e}")
                        
                        self.wait_for_operation(0.05)
            except Exception as e:
                print(f"❌ Error obteniendo {categoria}: {e}")
        
        print(f"\nLimpieza nuclear completada: {total_eliminados} elementos eliminados")
        return True

    def mostrar_resumen(self):
        """Muestra un resumen de lo creado"""
        self.print_header("RESUMEN DEL POBLADO DE BASE DE DATOS")
        
        print("ESTADÍSTICAS:")
        print(f"   ✅ Elementos creados exitosamente: {self.stats['created']}")
        print(f"   ❌ Errores durante la creación: {self.stats['errors']}")
        
        print("\nDATOS CREADOS:")
        for categoria, items in self.created_ids.items():
            print(f"   🎯 {categoria.capitalize()}: {len(items)} elementos")
        
        print(f"\n🎉 ¡Base de datos lista para la demo!")
        print("Puedes acceder a los datos en:")
        print(f"Usuarios: {BASE_URL}/usuarios/")
        print(f"Cervezas: {BASE_URL}/cervezas/")
        print(f"Cervecerías: {BASE_URL}/cervecerias/")
        print(f"Galardones: {BASE_URL}/galardones/")
        print(f"Degustaciones: {BASE_URL}/degustaciones/")

# --- Ejecución principal ---
if __name__ == "__main__":
    seeder = DatabaseSeeder()
    
    print("INICIANDO POBLADOR DE BASE DE DATOS BEERSP")
    print("Asegúrate de que el servidor Flask esté ejecutándose en http://localhost:8000")
    time.sleep(2)
    
    # Poblar la base de datos
    seeder.limpiar_todo_por_api()
    seeder.poblar_base_datos()
 
    # Para limpiar todo, descomenta las siguientes líneas:
    # print("\n" + "="*70)
    # input("Presiona Enter para limpiar toda la base de datos...")
    # seeder.limpiar_todo_por_api()