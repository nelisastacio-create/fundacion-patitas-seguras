from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "patitas_seguras_clave_secreta"

DB_NAME = "patitas_seguras.db"


def obtener_conexion():
    conexion = sqlite3.connect(DB_NAME)
    conexion.row_factory = sqlite3.Row
    return conexion


@app.route("/")
def inicio():
    if "usuario_id" not in session:
        return redirect(url_for("login"))
    return render_template("index.html", session=session)


@app.route("/historia")
def historia():
    if "usuario_id" not in session:
        return redirect(url_for("login"))
    return render_template("historia.html", session=session)


@app.route("/mascotas")
def mascotas():
    if "usuario_id" not in session:
        return redirect(url_for("login"))

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id, nombre, especie, raza, edad, sexo, estado_salud, descripcion, foto, estado_adopcion
        FROM animales_disponibles
        ORDER BY id ASC
    """)

    mascotas_data = cursor.fetchall()
    conexion.close()

    return render_template("mascotas.html", session=session, mascotas=mascotas_data)


@app.route("/formularios", methods=["GET", "POST"])
def formularios():
    if "usuario_id" not in session:
        return redirect(url_for("login"))

    mensaje = None

    if request.method == "POST":
        telefono = request.form.get("telefono")
        direccion = request.form.get("direccion")
        mascota = request.form.get("mascota")
        motivo = request.form.get("motivo")
        experiencia = request.form.get("experiencia")

        if not telefono or not direccion or not mascota or not motivo or not experiencia:
            mensaje = "Todos los campos obligatorios deben completarse."
        else:
            conexion = obtener_conexion()
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT id, estado_adopcion
                FROM animales_disponibles
                WHERE nombre = ?
            """, (mascota,))
            animal = cursor.fetchone()

            if not animal:
                conexion.close()
                mensaje = "La mascota seleccionada no existe en la base de datos."
                return render_template("formularios.html", session=session, mensaje=mensaje)

            if animal["estado_adopcion"] == "Adoptado":
                conexion.close()
                mensaje = "Esa mascota ya fue adoptada y no está disponible para nuevas solicitudes."
                return render_template("formularios.html", session=session, mensaje=mensaje)

            animal_id = animal["id"]

            cursor.execute("SELECT COUNT(*) AS total FROM solicitudes_adopcion")
            total = cursor.fetchone()["total"] + 1
            numero_solicitud = f"SOL-{total:04d}"

            fecha_actual = datetime.now().strftime("%Y-%m-%d")

            cursor.execute("""
                INSERT INTO solicitudes_adopcion
                (numero_solicitud, usuario_id, animal_id, telefono, direccion, motivo, experiencia_mascotas, estado, fecha)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                numero_solicitud,
                session["usuario_id"],
                animal_id,
                telefono,
                direccion,
                motivo,
                experiencia,
                "Pendiente",
                fecha_actual
            ))

            conexion.commit()
            conexion.close()

            return redirect(url_for("solicitudes"))

    return render_template("formularios.html", session=session, mensaje=mensaje)


@app.route("/solicitudes")
def solicitudes():
    if "usuario_id" not in session:
        return redirect(url_for("login"))

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    if session.get("usuario_rol") == "Administrador":
        cursor.execute("""
            SELECT s.id, s.numero_solicitud, s.telefono, s.direccion, s.motivo,
                   s.experiencia_mascotas, s.estado, s.fecha,
                   u.nombre AS usuario_nombre,
                   a.nombre AS animal_nombre
            FROM solicitudes_adopcion s
            JOIN usuarios u ON s.usuario_id = u.id
            JOIN animales_disponibles a ON s.animal_id = a.id
            ORDER BY s.id DESC
        """)
    else:
        cursor.execute("""
            SELECT s.id, s.numero_solicitud, s.telefono, s.direccion, s.motivo,
                   s.experiencia_mascotas, s.estado, s.fecha,
                   u.nombre AS usuario_nombre,
                   a.nombre AS animal_nombre
            FROM solicitudes_adopcion s
            JOIN usuarios u ON s.usuario_id = u.id
            JOIN animales_disponibles a ON s.animal_id = a.id
            WHERE s.usuario_id = ?
            ORDER BY s.id DESC
        """, (session["usuario_id"],))

    solicitudes_data = cursor.fetchall()
    conexion.close()

    return render_template(
        "solicitudes.html",
        session=session,
        solicitudes=solicitudes_data
    )


@app.route("/actualizar_solicitud/<int:solicitud_id>/<accion>", methods=["POST"])
def actualizar_solicitud(solicitud_id, accion):
    if "usuario_id" not in session:
        return redirect(url_for("login"))

    if session.get("usuario_rol") != "Administrador":
        return redirect(url_for("solicitudes"))

    if accion not in ["aceptar", "rechazar"]:
        return redirect(url_for("solicitudes"))

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id, animal_id, estado
        FROM solicitudes_adopcion
        WHERE id = ?
    """, (solicitud_id,))
    solicitud = cursor.fetchone()

    if not solicitud:
        conexion.close()
        return redirect(url_for("solicitudes"))

    animal_id = solicitud["animal_id"]

    if accion == "aceptar":
        cursor.execute("""
            UPDATE solicitudes_adopcion
            SET estado = 'Adoptado'
            WHERE id = ?
        """, (solicitud_id,))

        cursor.execute("""
            UPDATE animales_disponibles
            SET estado_adopcion = 'Adoptado'
            WHERE id = ?
        """, (animal_id,))

        cursor.execute("""
            UPDATE solicitudes_adopcion
            SET estado = 'Rechazada'
            WHERE animal_id = ?
              AND id != ?
              AND estado = 'Pendiente'
        """, (animal_id, solicitud_id))

    else:
        cursor.execute("""
            UPDATE solicitudes_adopcion
            SET estado = 'Rechazada'
            WHERE id = ?
        """, (solicitud_id,))

    conexion.commit()
    conexion.close()

    return redirect(url_for("solicitudes"))


@app.route("/eliminar_solicitud/<int:solicitud_id>", methods=["POST"])
def eliminar_solicitud(solicitud_id):
    if "usuario_id" not in session:
        return redirect(url_for("login"))

    if session.get("usuario_rol") != "Administrador":
        return redirect(url_for("solicitudes"))

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        DELETE FROM solicitudes_adopcion
        WHERE id = ?
    """, (solicitud_id,))

    conexion.commit()
    conexion.close()

    return redirect(url_for("solicitudes"))


@app.route("/login", methods=["GET", "POST"])
def login():
    mensaje = None

    if request.method == "POST":
        correo = request.form.get("correo")
        password = request.form.get("password")

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT * FROM usuarios
            WHERE correo = ? AND password = ?
        """, (correo, password))

        usuario = cursor.fetchone()
        conexion.close()

        if usuario:
            session["usuario_id"] = usuario["id"]
            session["usuario_nombre"] = usuario["nombre"]
            session["usuario_correo"] = usuario["correo"]
            session["usuario_rol"] = usuario["rol"]
            return redirect(url_for("inicio"))
        else:
            mensaje = "Credenciales incorrectas. Intenta de nuevo."

    return render_template("login.html", mensaje=mensaje)


@app.route("/registro", methods=["GET", "POST"])
def registro():
    mensaje = None

    if request.method == "POST":
        nombre = request.form.get("nombre")
        correo = request.form.get("correo")
        password = request.form.get("password")
        confirmar_password = request.form.get("confirmar_password")

        if not nombre or not correo or not password or not confirmar_password:
            mensaje = "Todos los campos son obligatorios."
        elif password != confirmar_password:
            mensaje = "Las contraseñas no coinciden."
        else:
            try:
                conexion = obtener_conexion()
                cursor = conexion.cursor()

                cursor.execute("""
                    INSERT INTO usuarios (nombre, correo, password, rol)
                    VALUES (?, ?, ?, ?)
                """, (nombre, correo, password, "Adoptante"))

                conexion.commit()
                conexion.close()

                return redirect(url_for("login"))
            except sqlite3.IntegrityError:
                mensaje = "Ese correo ya está registrado."

    return render_template("registro.html", mensaje=mensaje)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)