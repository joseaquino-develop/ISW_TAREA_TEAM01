from app.database import db


class Reserva(db.Model):
    __tablename__ = "reservas"

    id_reserva = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_cliente = db.Column(db.String(120), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    correo = db.Column(db.String(150), nullable=False)
    fecha_reserva = db.Column(db.Date, nullable=False)
    hora_reserva = db.Column(db.Time, nullable=False)
    numero_personas = db.Column(db.Integer, nullable=False)
    observaciones = db.Column(db.Text)
    estado = db.Column(db.String(30), nullable=False, default="Pendiente")
    fecha_registro = db.Column(
        db.DateTime,
        server_default=db.func.current_timestamp()
    )