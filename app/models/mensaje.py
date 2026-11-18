from app.database import db


class Mensaje(db.Model):
    __tablename__ = "mensajes_contacto"

    id_mensaje = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(120), nullable=False)
    correo = db.Column(db.String(150), nullable=False)
    telefono = db.Column(db.String(20))
    asunto = db.Column(db.String(150), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)
    estado = db.Column(db.String(30), nullable=False, default="Nuevo")
    fecha_registro = db.Column(
        db.DateTime,
        server_default=db.func.current_timestamp()
    )