from dao import db,Base

class EquipeModel(Base):
    __tablename__ = 'equipes'
    id = db.Column(db.Integer, primary_key=True)
    id_demanda = db.Column(db.Integer, db.ForeignKey('demandas.id'), nullable=False)
    prazo = db.Column(db.DateTime, nullable=False)
    orcamento = db.Column(db.Float, nullable=False)
    id_integrador = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    id_cliente = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    titulo = db.Column(db.String(200), nullable=False)
    id_equipe = db.Column(db.Integer, db.ForeignKey('equipes.id'), nullable=False)
    id_servico = db.Column(db.Integer, db.ForeignKey('servicos.id'), nullable=False)
    descricao = db.Column(db.String(200))
    status = db.Column(db.String(20), nullable=False)

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
