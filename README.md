# FastAPI REST API - Usuarios y Productos 

API RESTful desarrollada con **FastAPI** que implementa autenticación segura JWT, persistencia de datos relacional y gestión de usuarios con sus respectivos productos asociados.

---

## 🛠️ Tecnologías Utilizadas

* **Framework:** FastAPI
* **Base de Datos:** SQLite (SQLAlchemy ORM)
* **Autenticación & Seguridad:** JWT (JSON Web Tokens), Bcrypt (Hashing de contraseñas), `python-dotenv`
* **Validación de Datos:** Pydantic (v2)
* **Servidor ASGI:** Uvicorn

---

## 📋 Características Principales

*  **Seguridad Avanzada:** Encriptación de contraseñas con `bcrypt` (limitado a 72 bytes de forma segura) y expiración de tokens JWT en 30 minutos.
*  **Rutas Protegidas:** Middlewares de autenticación mediante esquema `HTTPBearer` para verificar tokens en endpoints privados.
*  **Relaciones ORM:** Relación 1:N entre la tabla `usuarios` y `productos` (Un usuario posee múltiples productos registrados).
*  **CORS Habilitado:** Middleware configurado para permitir peticiones cross-origin.

---

##  Instalación y Configuración Local

### 1. Clonar el repositorio
```bash
git clone [https://github.com/Christopher-Zambrano/ApiRest-Usuarios-Productos.git](https://github.com/Christopher-Zambrano/ApiRest-Usuarios-Productos.git)
cd ApiRest-Usuarios-Productos
