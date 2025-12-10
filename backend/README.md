# BeerSP - Documentación del backend

## Descripción General

Backend desarrollado para la aplicación BeerSP, una plataforma social para amantes de la cerveza que permite registrar degustaciones, gestionar perfiles de usuarios, y otorgar galardones por actividades cerveceras.

## Arquitectura del Proyecto

```
backend/
├── app/
│   ├── controladores/          # Controladores Flask (Rutas API)
│   │   ├── cerveza_controlador.py
│   │   ├── usuario_controlador.py
│   │   ├── galardon_controlador.py
│   │   ├── cerveceria_controlador.py
│   │   └── degustacion_controlador.py
│   ├── objetos/                #  Modelos SQLAlchemy
│   │   ├── cerveza.py
│   │   ├── usuario.py
│   │   ├── galardon.py
│   │   ├── cerveceria.py
│   │   ├── degustacion.py
│   │   └── amistad.py
│   ├── servicios/              # Lógica de negocio
│   │   ├── cerveza_servicio.py
│   │   ├── usuario_servicio.py
│   │   ├── galardon_servicio.py
│   │   ├── cerveceria_servicio.py
│   │   └── degustacion_servicio.py
│   ├── __init__.py
│   ├── app.py                 # Aplicación  principal
│   ├── base_datos.py          # Configuración de base de datos
│   └── database.db           # Base de datos SQLite
├── tests/                     # Pruebas automatizadas
    ├── cerveza_tester.py
    ├── galardon_tester.py
    └── usuario_tester.py
```

## Tecnologías y Librerías

### **Framework Principal**
- **Flask** - Microframework web para Python
- **Flask-CORS** - Manejo de CORS para peticiones cross-origin

### **Base de Datos y ORM**
- **SQLAlchemy** - ORM para mapeo objeto-relacional
- **SQLite** - Base de datos embebida (desarrollo)
- **StaticPool** - Pool de conexiones para SQLite

### **Librerías de Desarrollo**
- **requests** - Cliente HTTP para pruebas
- **json** - Manejo de datos JSON para inputs y outputs del sistema

## Estructura de Capas

### **1. Capa de Modelos (`objetos/`)**
- **Base**: `declarative_base()` de SQLAlchemy
- **Modelos**: 
  - `Cerveza`, `Usuario`, `Galardon`, `Cerveceria`, `Degustacion`
  - Método `to_dict()` para serialización JSON

### **2. Capa de Servicios (`servicios/`)**
- **Patrón Service**: Lógica de negocio separada
- **Métodos estáticos**: Para operaciones de base de datos
- **Validaciones**: Reglas de negocio y validaciones

### **3. Capa de Controladores (`controladores/`)**
- **Blueprints**: Modularización de rutas Flask
- **Rutas RESTful**: Endpoints HTTP bien definidos
- **Manejo de errores**: Códigos HTTP apropiados

### **4. Configuración de BD (`base_datos.py`)**
- **SessionLocal**: Fábrica de sesiones SQLAlchemy
- **init_db()**: Inicialización de tablas
- **get_db()**: Gestión de sesiones por request

## Endpoints Principales

### **Cervezas (`/api/cervezas/`)**
- `POST /` - Crear cerveza 
- `GET /` - Buscar y filtrar cervezas 
- `GET /<id>/` - Detalles de una cerveza
- `GET /estilos/` - Lista de estilos únicos 
- `GET /paises/` - Lista de países únicos

### **Usuarios (`/api/usuarios/`)**
- `POST /` - Registrar usuario (RF-1.2)
- `GET /` - Listar usuarios
- `GET /<id>/` - Obtener usuario por ID
- `PUT /<id>/` - Actualizar perfil (RF-1.7)
- `DELETE /<id>/` - Eliminar usuario
- `GET /<id>/galardones` - Galardones de un usuario 

### **Amistades (`/api/usuarios/<id>/amigos/`)**
- `POST /` - Agregar amigo (RF-2.2)
- `GET /` - Listar amigos (RF-2.6)
- `DELETE /<friend_id>/` - Eliminar amigo

### **Galardones (`/api/galardones/`)**
- `POST /` - Crear galardón 
- `GET /` - Listar galardones

## Configuración y Ejecución

### **Requisitos del Sistema**
Python 3.8+
pip install requirements.txt

### **Ejecución en Desarrollo**

# Desde el directorio backend/
python -m app.main


### **Inicialización de Base de Datos**
La base de datos se inicializa automáticamente al ejecutar la aplicación:

### **Comandos sqlite**
- **Acceder base de datos**: "sqlite3 database.db"
- **Mostrar bases de datos**: ".databases"

## Sistema de Pruebas

### **Ejecutar Pruebas**

# Pruebas de Cervezas
python tests/cerveza_tester.py

# Pruebas de Galardones  
python tests/galardon_tester.py

# Pruebas de Usuarios
python tests/usuario_tester.py

### **Características de las Pruebas**
- **Limpieza automática**: Borra datos de prueba al finalizar
- **Diagnóstico**: Verifica endpoints disponibles
- **Validación**: Comprueba códigos HTTP y respuestas
- **Robustez**: Manejo de errores y timeouts

## Características Técnicas

### **Patrones de Diseño Implementados**
- **MVC** (Modelo-Vista-Controlador)
- **Repository Pattern** (a través de servicios)
- **Dependency Injection** (sesiones de BD)
- **RESTful API Design**

### **Características de Seguridad**
- **CORS** habilitado para desarrollo
- **Validación** de datos de entrada
- **Manejo seguro** de contraseñas (no se devuelven en respuestas)
- **Control de duplicados** en registros

## Flujo de Datos Típico

1. **Request HTTP** → Controlador
2. **Validación** → Servicio  
3. **Lógica de negocio** → Servicio
4. **Operaciones BD** → Modelo SQLAlchemy
5. **Serialización** → `to_dict()`
6. **Response JSON** → Cliente
