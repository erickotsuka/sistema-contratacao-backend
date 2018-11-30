from dao import db,Base

class UsuarioModel(Base):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    tipoUsuario = db.Column(db.String(20), nullable=False)
    nome = db.Column(db.String(200), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    cargo = db.Column(db.String(200), nullable=False)
    telefone = db.Column(db.String(200), nullable=True)
    foto = db.Column(db.String(200), nullable=False)
    avaliacao = db.Column(db.Integer, nullable=False)

    def __init__(self, nome):
        self.nome = nome

    def adicionar(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def encontrar_pelo_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def encontrar_pelo_nome(cls, nome):
        return cls.query.filter_by(nome=nome).first()

    @classmethod
    def listar(cls):
        return cls.query.all()

    def remover(self):
        db.session.delete(self)
        db.session.commit()
