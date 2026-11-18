from app.models.plato import Plato


def listar_platos():
    return (
        Plato.query
        .filter_by(disponible=True)
        .order_by(Plato.id_plato.desc())
        .all()
    )