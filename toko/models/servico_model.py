from dao import db,Base

class ServicoModel(Base):
    __tablename__ = 'servicos'
    id = db.Column(db.Integer, primary_key=True)
    id_proposta = db.Column(db.Integer, db.ForeignKey('propostas.id'))
    nome = db.Column(db.String(200))
    descricao = db.Column(db.String(200))
    id_cronograma = db.Column(db.Integer, db.ForeignKey('cronogramas.id'))

    def __init__(self, nome):
        self.nome = nome

    def adicionar(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def encontrar_pelo_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def encontrar_pelo_titulo(cls, titulo):
        return cls.query.filter_by(titulo=titulo).all()

    @classmethod
    def listar(cls):
        return cls.query.all()

    def remover(self):
        db.session.delete(self)
        db.session.commit()
