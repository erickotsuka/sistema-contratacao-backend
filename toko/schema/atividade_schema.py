from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

from toko.models.atividade_model import AtividadeModel
class AtividadeSchema(ModelSchema):
    class Meta:
        model = AtividadeModel
