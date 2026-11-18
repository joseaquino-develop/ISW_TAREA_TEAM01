from app.database import db


class Categoria(db.Model):
    __tablename__ = "categorias"

    id_categoria = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    descripcion = db.Column(db.String(255))
    estado = db.Column(db.Boolean, nullable=False, default=True)

    platos = db.relationship("Plato", back_populates="categoria")