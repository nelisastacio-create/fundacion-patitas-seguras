import sqlite3

DB_NAME = "patitas_seguras.db"

def crear_base_datos():
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()

    # Tabla de usuarios
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        correo TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        rol TEXT NOT NULL CHECK(rol IN ('Administrador', 'Adoptante'))
    )
    """)

    # Tabla de animales disponibles
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS animales_disponibles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        especie TEXT NOT NULL,
        raza TEXT NOT NULL,
        edad INTEGER NOT NULL,
        sexo TEXT NOT NULL,
        estado_salud TEXT NOT NULL,
        descripcion TEXT,
        foto TEXT,
        estado_adopcion TEXT NOT NULL DEFAULT 'Disponible'
    )
    """)

    # Tabla de solicitudes de adopción
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS solicitudes_adopcion (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        numero_solicitud TEXT NOT NULL UNIQUE,
        usuario_id INTEGER NOT NULL,
        animal_id INTEGER NOT NULL,
        telefono TEXT NOT NULL,
        direccion TEXT NOT NULL,
        motivo TEXT NOT NULL,
        experiencia_mascotas TEXT NOT NULL,
        estado TEXT NOT NULL DEFAULT 'Pendiente',
        fecha TEXT NOT NULL,
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
        FOREIGN KEY (animal_id) REFERENCES animales_disponibles(id)
    )
    """)

    conexion.commit()
    conexion.close()
    print("Base de datos creada correctamente con 3 tablas.")

if __name__ == "__main__":
    crear_base_datos() 