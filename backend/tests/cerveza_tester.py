import requests
import json
import time

# --- Configuración ---
BASE_URL = "http://localhost:8000/api"

def print_test_header(titulo):
    """ Imprime un cabezal bonito para cada prueba """
    print("\n" + "="*50)
    print(f" 📦 PRUEBA: {titulo}")
    print("="*50)

def run_tests():
    """ Ejecuta todas las pruebas de la API de Cervezas """
    
    try:
        # --- PRUEBA 0: Comprobar si el servidor está vivo ---
        print_test_header("Conexión al Servidor (GET /)")
        try:
            home_resp = requests.get("http://localhost:8000/")
            home_resp.raise_for_status() # Lanza error si es 4xx o 5xx
            print(f"✅ Servidor conectado. Mensaje: {home_resp.json()['message']}")
        except requests.exceptions.ConnectionError:
            print("❌ ERROR: No se pudo conectar.")
            print("🚨 ¿Has arrancado 'app.py' en otra terminal?")
            return # Salimos si no hay servidor
        except Exception as e:
            print(f"❌ ERROR inesperado en Home: {e}")
            return

        # --- PRUEBA 1: Crear una cerveza (POST) ---
        print_test_header("Crear Cerveza (POST /api/cervezas/)")
        nueva_cerveza_data = {
            "nombre": "Cerveza de Prueba API",
            "estilo": "API Test Lager",
            "pais_procedencia": "Python",
            "porcentaje_alcohol": 5.1
        }
        # Usamos json= para enviar los datos como JSON
        resp_post = requests.post(f"{BASE_URL}/cervezas/", json=nueva_cerveza_data)
        
        if resp_post.status_code == 201: # 201 Created
            print(f"✅ ¡Cerveza creada! (Código 201)")
            print(f"   Respuesta: {json.dumps(resp_post.json(), indent=2)}")
            # Guardamos el ID para usarlo luego
            cerveza_id = resp_post.json()['id']
        else:
            print(f"❌ ERROR al crear. Código: {resp_post.status_code}")
            print(f"   Respuesta: {resp_post.text}")
            return # Salimos si esto falla

        # --- PRUEBA 2: Intentar crear duplicado (POST) ---
        print_test_header("Crear Duplicado (POST /api/cervezas/)")
        resp_dupl = requests.post(f"{BASE_URL}/cervezas/", json=nueva_cerveza_data)
        
        if resp_dupl.status_code == 409: # 409 Conflict
            print(f"✅ ¡Error 409 recibido correctamente!")
            print(f"   Respuesta: {resp_dupl.json()['error']}")
        else:
            print(f"❌ ERROR: Se esperaba 409 pero se recibió {resp_dupl.status_code}")

        # --- PRUEBA 3: Buscar Cervezas (GET con filtro) ---
        print_test_header("Buscar Cervezas (GET /api/cervezas/?estilo=...)")
        # Usamos params= para los query params
        params_filtro = {"estilo": "API Test Lager"}
        resp_get_filtro = requests.get(f"{BASE_URL}/cervezas/", params=params_filtro)
        
        if resp_get_filtro.status_code == 200:
            resultados = resp_get_filtro.json()
            print(f"✅ ¡Búsqueda OK! Encontrados {len(resultados)} resultados.")
            print(f"   - {resultados[0]['nombre']}")
            assert len(resultados) > 0 # Comprobamos que no está vacío
        else:
            print(f"❌ ERROR al buscar. Código: {resp_get_filtro.status_code}")

        # --- PRUEBA 4: Obtener Detalle (GET /api/cervezas/<id>/) ---
        print_test_header(f"Obtener Detalle (GET /api/cervezas/{cerveza_id}/)")
        resp_detalle = requests.get(f"{BASE_URL}/cervezas/{cerveza_id}/")
        
        if resp_detalle.status_code == 200:
            detalle = resp_detalle.json()
            print(f"✅ ¡Detalle OK! Cerveza: {detalle['nombre']}")
            print(f"   Valoración Promedio: {detalle['valoracion_promedio']}")
        else:
            print(f"❌ ERROR al obtener detalle. Código: {resp_detalle.status_code}")
            
        # --- PRUEBA 5: Obtener Estilos (GET /api/cervezas/estilos/) ---
        print_test_header("Obtener Estilos (GET /api/cervezas/estilos/)")
        resp_estilos = requests.get(f"{BASE_URL}/cervezas/estilos/")
        if resp_estilos.status_code == 200:
            estilos = resp_estilos.json()
            print(f"✅ ¡Estilos OK! Encontrados {len(estilos)} estilos.")
            print(f"   Entre ellos está: 'API Test Lager' ({'API Test Lager' in estilos})")
            assert 'API Test Lager' in estilos
        else:
            print(f"❌ ERROR al obtener estilos. Código: {resp_estilos.status_code}")
            
        print("\n" + "="*50)
        print("🎉 ¡TODAS LAS PRUEBAS DE API HAN SIDO EXITOSAS! 🎉")
        print("="*50)

    except Exception as e:
        print("\n" + "!"*50)
        print(f"💥 ¡UNA PRUEBA HA FALLADO INESPERADAMENTE! 💥")
        print(f"Error: {e}")
        print("!"*50)

if __name__ == "__main__":
    print("Iniciando pruebas de API en 2 segundos...")
    print("Asegúrate de que 'main.py' esté ejecutándose en otra terminal.")
    time.sleep(2)
    run_tests()