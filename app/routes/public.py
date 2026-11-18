from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy.exc import SQLAlchemyError
from types import SimpleNamespace

from app.models.categoria import Categoria
from app.services.plato_service import listar_platos
from app.services.reserva_service import registrar_reserva
from app.services.mensaje_service import registrar_mensaje

public_bp = Blueprint("public", __name__)


@public_bp.route("/")
def inicio():
    return render_template("inicio.html")


@public_bp.route("/nosotros")
def nosotros():
    return render_template("nosotros.html")


@public_bp.route("/carta")
def carta():
    carta_demo = False
    try:
        platos = listar_platos()
        categorias = Categoria.query.filter_by(estado=True).order_by(
            Categoria.nombre
        ).all()
    except SQLAlchemyError:
        platos = []
        categorias = []
        carta_demo = True

    if not platos:
        carta_demo = True
        categorias_demo = [
            SimpleNamespace(id_categoria="demo-arroces", nombre="Arroces"),
            SimpleNamespace(id_categoria="demo-tallarines", nombre="Tallarines"),
            SimpleNamespace(id_categoria="demo-entradas", nombre="Entradas"),
        ]
        platos_demo = [
            ("demo-arroz", "demo-arroces", "Arroz chaufa clásico", "Arroz salteado al wok con huevo, cebolla china y sillao.", "photo-1512058564366-18510be2db19"),
            ("demo-arroz-pollo", "demo-arroces", "Chaufa de pollo", "Una opción clásica con pollo, arroz y verduras salteadas.", "photo-1603133872878-684f208fb84b"),
            ("demo-arroz-mixto", "demo-arroces", "Chaufa mixto", "Combinación de pollo y carne al estilo chifa.", "photo-1603133872878-684f208fb84b"),
            ("demo-tallarin-saltado", "demo-tallarines", "Tallarín saltado", "Tallarines al wok con verduras frescas y salsa de la casa.", "photo-1569718212165-3a8278d5f624"),
            ("demo-tallarin-pollo", "demo-tallarines", "Tallarín con pollo", "Tallarines salteados con pollo y vegetales.", "photo-1569718212165-3a8278d5f624"),
            ("demo-aeropuerto", "demo-arroces", "Aeropuerto", "Arroz y tallarín salteados al wok en un solo plato.", "photo-1512058564366-18510be2db19"),
            ("demo-wantan", "demo-entradas", "Wantán frito", "Bocados crocantes para empezar y compartir.", "photo-1563245372-f21724e3856d"),
            ("demo-rollitos", "demo-entradas", "Rollitos primavera", "Rollitos dorados con relleno de verduras.", "photo-1563245372-f21724e3856d"),
        ]
        categoria_por_id = {categoria.id_categoria: categoria for categoria in categorias_demo}
        platos = [
            SimpleNamespace(
                id_plato=identificador,
                id_categoria=categoria_id,
                categoria=categoria_por_id[categoria_id],
                nombre=nombre,
                descripcion=descripcion,
                precio=None,
                imagen_url=f"https://images.unsplash.com/{imagen}?auto=format&fit=crop&w=900&q=85",
            )
            for identificador, categoria_id, nombre, descripcion, imagen in platos_demo
        ]
        categorias = categorias_demo

    return render_template(
        "carta.html", platos=platos, categorias=categorias, carta_demo=carta_demo
    )


@public_bp.route("/promociones")
def promociones():
    return render_template("promociones.html")


@public_bp.route("/reservas")
def reservas():
    return render_template("reservas.html")


@public_bp.route("/galeria")
def galeria():
    return render_template("galeria.html")


@public_bp.route("/contacto")
def pagina_contacto():
    asuntos_validos = {
        "Consulta general", "Eventos", "Pedidos especiales", "Promociones", "Otros"
    }
    asunto = request.args.get("asunto", "")
    return render_template(
        "contacto.html",
        asunto_inicial=asunto if asunto in asuntos_validos else "",
        mensaje_inicial=request.args.get("mensaje", "")[:1000]
    )


@public_bp.route("/reservar", methods=["POST"])
def reservar():
    try:
        datos = {
            "nombre_cliente": request.form.get("nombre_cliente", ""),
            "telefono": request.form.get("telefono", ""),
            "correo": request.form.get("correo", ""),
            "fecha_reserva": request.form.get("fecha_reserva", ""),
            "hora_reserva": request.form.get("hora_reserva", ""),
            "numero_personas": request.form.get("numero_personas", ""),
            "observaciones": request.form.get("observaciones", "")
        }

        if not all([
            datos["nombre_cliente"].strip(),
            datos["telefono"].strip(),
            datos["correo"].strip(),
            datos["fecha_reserva"],
            datos["hora_reserva"],
            datos["numero_personas"]
        ]):
            raise ValueError("Completa todos los campos obligatorios.")

        reserva = registrar_reserva(datos)

        return render_template(
            "confirmacion.html",
            titulo="¡Solicitud recibida!",
            mensaje=(
                f"Gracias, {reserva.nombre_cliente}. "
                "Tu solicitud de reserva fue registrada y está pendiente "
                "de confirmación."
            )
        )

    except (ValueError, TypeError) as error:
        flash(str(error), "error")
    except SQLAlchemyError:
        from app.database import db
        db.session.rollback()
        flash("No se pudo guardar la reserva. Inténtalo nuevamente.", "error")

    return redirect(url_for("public.reservas"))


@public_bp.route("/contacto", methods=["POST"])
def contacto():
    try:
        datos = {
            "nombre": request.form.get("nombre", ""),
            "correo": request.form.get("correo", ""),
            "telefono": request.form.get("telefono", ""),
            "asunto": request.form.get("asunto", ""),
            "mensaje": request.form.get("mensaje", "")
        }

        if not all([
            datos["nombre"].strip(),
            datos["correo"].strip(),
            datos["asunto"].strip(),
            datos["mensaje"].strip()
        ]):
            raise ValueError("Completa los campos obligatorios del formulario.")

        registrar_mensaje(datos)

        return render_template(
            "confirmacion.html",
            titulo="¡Mensaje enviado!",
            mensaje="Gracias por comunicarte con CHIFA FUSION. "
                    "Hemos registrado tu consulta."
        )

    except ValueError as error:
        flash(str(error), "error")
    except SQLAlchemyError:
        from app.database import db
        db.session.rollback()
        flash("No se pudo guardar tu mensaje. Inténtalo nuevamente.", "error")

    return redirect(url_for("public.pagina_contacto"))
