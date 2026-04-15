import sqlite3

DB_NAME = "patitas_seguras.db"

def insertar_usuarios():
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()

    usuarios = [
        ("Administrador Principal", "admin@patitasseguras.com", "Admin123!", "Administrador"),
        ("Adoptante Demo", "adoptante@patitasseguras.com", "Adopt123!", "Adoptante")
    ]

    for usuario in usuarios:
        try:
            cursor.execute("""
                INSERT INTO usuarios (nombre, correo, password, rol)
                VALUES (?, ?, ?, ?)
            """, usuario)
        except sqlite3.IntegrityError:
            print(f"El usuario {usuario[1]} ya existe.")

    conexion.commit()
    conexion.close()
    print("Usuarios insertados correctamente.")

if __name__ == "__main__":
    insertar_usuarios()