from dao import db,Base

class DemandaModel(Base):
    __tablename__ = 'demandas'
    id = db.Column(db.Integer, primary_key=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    titulo = db.Column(db.String(200), nullable=False)
    tipo_servico = db.Column(db.String(200), nullable=False)
    data_limite = db.Column(db.DateTime, nullable=True)
    descricao = db.Column(db.String(200))

    def __init__(self, id_cliente, titulo, tipo_servico, data_limite, descricao):
        self.id_cliente = id_cliente
        self.titulo = titulo
        self.tipo_servico = tipo_servico
        self.data_limite = data_limite
        self.descricao =  descricao

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
