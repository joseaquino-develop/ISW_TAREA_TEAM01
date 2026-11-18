from datetime import date, time
from app.database import db
from app.models.reserva import Reserva


def registrar_reserva(datos):
    fecha = date.fromisoformat(datos["fecha_reserva"])
    hora = time.fromisoformat(datos["hora_reserva"])
    personas = int(datos["numero_personas"])

    if fecha < date.today():
        raise ValueError("La fecha de reserva no puede estar en el pasado.")

    if personas < 1 or personas > 30:
        raise ValueError("El número de personas debe estar entre 1 y 30.")

    reserva = Reserva(
        nombre_cliente=datos["nombre_cliente"].strip(),
        telefono=datos["telefono"].strip(),
        correo=datos["correo"].strip(),
        fecha_reserva=fecha,
        hora_reserva=hora,
        numero_personas=personas,
        observaciones=datos.get("observaciones", "").strip()
    )

    db.session.add(reserva)
    db.session.commit()

    return reserva