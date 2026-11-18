from app.database import db
from app.models.mensaje import Mensaje


def registrar_mensaje(datos):
    mensaje = Mensaje(
        nombre=datos["nombre"].strip(),
        correo=datos["correo"].strip(),
        telefono=datos.get("telefono", "").strip(),
        asunto=datos["asunto"].strip(),
        mensaje=datos["mensaje"].strip()
    )

    db.session.add(mensaje)
    db.session.commit()

    return mensaje