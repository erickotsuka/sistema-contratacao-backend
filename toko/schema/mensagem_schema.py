from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

from toko.models.mensagem_model import MensagemModel
class MensagemSchema(ModelSchema):
    class Meta:
        model = MensagemModel
