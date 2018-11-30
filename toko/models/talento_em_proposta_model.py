from dao import db,Base

class TalentoEmPropostaModel(Base):
    __tablename__ = 'talento_em_proposta'
    id_talento = db.Column(db.Integer, db.ForeignKey('usuarios.id'), primary_key=True)
    id_proposta = db.Column(db.Integer, db.ForeignKey('propostas.id'), primary_key=True)

    def __init__(self, nome):
        self.nome = nome

    def adicionar(self):
        db.session.add(self)
        db.session.commit()

    def remover(self):
        db.session.delete(self)
        db.session.commit()
