from dao import db,Base

class MensagemModel(Base):
    __tablename__ = 'mensagens'
    id = db.Column(db.Integer, primary_key=True)
    id_chat = db.Column(db.Integer, nullable=False)
    id_usuario_de = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    id_usuario_para = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    data_hora = db.Column(db.DateTime, nullable=False)
    conteudo = db.Column(db.String(200), nullable=False)

    def __init__(self, id_chat, id_usuario_de, id_usuario_para, data_hora, conteudo):
        self.id_chat = id_chat
        self.id_usuario_de = id_usuario_de
        self.id_usuario_para = id_usuario_para
        self.data_hora = data_hora
        self.conteudo = conteudo

    def adicionar(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def encontrar_pelo_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def listar_por_id_chat(cls, _id_chat):
        return cls.query.filter_by(id_chat=_id_chat).order_by(cls.data_hora.asc()).all()

    @classmethod
    def listar(cls):
        return cls.query.all()

    def remover(self):
        db.session.delete(self)
        db.session.commit()
