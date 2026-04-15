# Fundación Patitas Seguras

Aplicación web desarrollada con Flask para la gestión de adopciones de mascotas.

## Funcionalidades
- Inicio de sesión
- Manejo de sesiones
- Registro de usuarios adoptantes
- Visualización de mascotas disponibles
- Formulario de adopción
- Gestión de solicitudes por parte del administrador
- Cambio automático de estado de mascota a Adoptado
- Eliminación de solicitudes antiguas por parte del administrador

## Tecnologías usadas
- Python
- Flask
- SQLite
- HTML
- CSS

## Credenciales de prueba

### Administrador
- Correo: admin@patitasseguras.com
- Contraseña: Admin123!

### Adoptante
- Correo: adoptante@patitasseguras.com
- Contraseña: Adopt123!

## Archivos principales
- app.py
- insertar_animales.py
- insertar_usuarios.py
- patitas_seguras.db

## Ejecución local
Ejecutar:
python3 app.py

Luego abrir en el navegador:
http://127.0.0.1:5000

## Estructura del proyecto
- templates/ : vistas HTML
- static/ : imágenes y recursos estáticos
- patitas_seguras.db : base de datos SQLite

## Nota
Proyecto académico para evaluación final de Pruebas Estáticas y Dinámicas de Seguridad a Aplicaciones (SAST/DAST).
