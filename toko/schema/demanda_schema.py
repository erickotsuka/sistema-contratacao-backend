from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

from toko.models.demanda_model import DemandaModel
class DemandaSchema(ModelSchema):
    class Meta:
        model = DemandaModel
