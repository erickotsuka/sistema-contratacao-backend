from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

from toko.models.usuario_model import UsuarioModel
class UsuarioSchema(ModelSchema):
    class Meta:
        model = UsuarioModel
