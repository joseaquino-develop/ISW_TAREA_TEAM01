from app.database import db


class Plato(db.Model):
    __tablename__ = "platos"

    id_plato = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_categoria = db.Column(
        db.Integer,
        db.ForeignKey("categorias.id_categoria"),
        nullable=False
    )

    nombre = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text)
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    imagen_url = db.Column(db.String(500))
    disponible = db.Column(db.Boolean, nullable=False, default=True)

    fecha_registro = db.Column(
        db.DateTime,
        server_default=db.func.current_timestamp()
    )

    fecha_actualizacion = db.Column(
        db.DateTime,
        server_default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )

    categoria = db.relationship("Categoria", back_populates="platos")