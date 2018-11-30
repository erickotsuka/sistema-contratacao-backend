from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

from toko.models.proposta_model import PropostaModel
class PropostaSchema(ModelSchema):
    class Meta:
        model = PropostaModel
