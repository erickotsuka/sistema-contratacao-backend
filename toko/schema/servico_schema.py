from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

from toko.models.servico_model import ServicoModel
class ServicoSchema(ModelSchema):
    class Meta:
        model = ServicoModel
