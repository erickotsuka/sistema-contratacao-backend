from dao import db,Base

class ServicoModel(Base):
    __tablename__ = 'servicos'
    id = db.Column(db.Integer, primary_key=True)
    id_proposta = db.Column(db.Integer, db.ForeignKey('propostas.id'))
    titulo = db.Column(db.String(200))
    descricao = db.Column(db.String(200))
    id_cronograma = db.Column(db.Integer)

    def __init__(self, id_proposta, titulo, descricao, id_cronograma):
        self.id_proposta = id_proposta
        self.titulo = titulo
        self.descricao = descricao
        self.id_cronograma = id_cronograma

    def adicionar(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def encontrar_pelo_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def encontrar_pelo_titulo(cls, titulo):
        return cls.query.filter_by(titulo=titulo).first()

    @classmethod
    def listar(cls):
        return cls.query.all()

    def remover(self):
        db.session.delete(self)
        db.session.commit()
