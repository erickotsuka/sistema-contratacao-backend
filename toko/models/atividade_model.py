from dao import db,Base

class AtividadeModel(Base):
    __tablename__ = 'atividades'
    id = db.Column(db.Integer, primary_key=True)
    id_cronograma = db.Column(db.Integer, nullable=False)
    nome = db.Column(db.String(200), nullable=False)
    entrega = db.Column(db.DateTime, nullable=False)
    descricao = db.Column(db.String(200))

    def __init__(self, nome):
        self.nome = nome

    def adicionar(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def encontrar_pelo_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def encontrar_pelo_nome(cls, _nome):
        return cls.query.filter_by(nome=_nome).all()

    @classmethod
    def lista_pelo_id_cronograma(cls, _id_cronograma):
        return cls.query.filter_by(id_cronograma=_id_cronograma).all()

    @classmethod
    def listar(cls):
        return cls.query.all()

    def remover(self):
        db.session.delete(self)
        db.session.commit()
