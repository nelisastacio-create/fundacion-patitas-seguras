import sqlite3

DB_NAME = "patitas_seguras.db"

def insertar_animales():
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()

    animales = [
        ("Luna", "Perro", "Mestiza", 2, "Hembra", "Sana", "Perrita cariñosa y juguetona", "luna.jpg", "Disponible"),
        ("Milo", "Gato", "Criollo", 1, "Macho", "Sano", "Gatito tranquilo y adaptable", "milo.jpg", "Disponible"),
        ("Nina", "Perro", "Pug", 3, "Hembra", "En tratamiento", "Perrita rescatada recientemente", "nina.jpg", "Disponible"),
        ("Canela", "Perro", "Mestiza", 2, "Hembra", "Sana", "Perrita noble y cariñosa", "canela.jpg", "Disponible")
    ]

    insertados = 0
    existentes = 0

    for animal in animales:
        nombre = animal[0]

        cursor.execute(
            "SELECT id FROM animales_disponibles WHERE nombre = ?",
            (nombre,)
        )
        existe = cursor.fetchone()

        if existe:
            existentes += 1
        else:
            cursor.execute("""
                INSERT INTO animales_disponibles
                (nombre, especie, raza, edad, sexo, estado_salud, descripcion, foto, estado_adopcion)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, animal)
            insertados += 1

    conexion.commit()
    conexion.close()

    print(f"Proceso completado. Insertados: {insertados}. Ya existentes: {existentes}.")

if __name__ == "__main__":
    insertar_animales()