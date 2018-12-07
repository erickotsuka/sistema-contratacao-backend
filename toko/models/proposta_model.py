from dao import db,Base

class PropostaModel(Base):
    __tablename__ = 'propostas'
    id = db.Column(db.Integer, primary_key=True)
    id_demanda = db.Column(db.Integer, db.ForeignKey('demandas.id'), nullable=False)
    prazo = db.Column(db.DateTime, nullable=False)
    orcamento = db.Column(db.Float, nullable=False)
    id_integrador = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    titulo = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.String(200))
    status = db.Column(db.String(20), nullable=False)

    def __init__(self, id_demanda, prazo, orcamento, id_integrador, titulo, descricao, status):
        self.id_demanda = id_demanda
        self.prazo = prazo
        self.orcamento = orcamento
        self.id_integrador = id_integrador
        self.titulo = titulo
        self.descricao = descricao
        self.status = status

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
