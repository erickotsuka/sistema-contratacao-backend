from flask_restful import Resource, reqparse, abort
from flask import request
from toko.models.usuario_model import UsuarioModel
from toko.schemas.usuario_schema import UsuarioSchema

class UsuarioResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("nome",
                        type=str,
                        required=True,
                        help="O nome do Usuario não pode estar em branco."
                        )
    parser.add_argument("tipoUsuario",
                        type=str,
                        required=True,
                        help="O tipo de Usuário não pode estar em branco."
                        )
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help="O email do Usuario não pode estar em branco."
                        )
    parser.add_argument('senha',
                        type=str,
                        required=True,
                        help="A senha do Usuario não pode estar em branco."
                        )
    parser.add_argument('cargo',
                        type=str,
                        required=True,
                        help="O cargo do Usuario não pode estar em branco."
                        )
    parser.add_argument('telefone',
                        type=str,
                        required=False,
                        help="O telefone do Usuário é opcional."
                        )
    parser.add_argument('foto',
                        type=str,
                        required=False,
                        help="A foto do usuário é opcional."
                        )
    parser.add_argument('avaliacao',
                        type=float,
                        required=False,
                        help="A avaliação do usuário é  opcional."
                        )

    def get(self,nome):
        json = ''
        try:
            usuario = UsuarioModel.encontrar_pelo_nome(nome)
            print(usuario)
            if usuario:
                schema = UsuarioSchema()
                json = schema.dump(usuario).data
            else:
                return {"message":"Usuario {} não existe".format(nome)},404
        except Exception as e:
            print(e)
            return {"message","Erro na requisição".format(nome)},500

        return json,200

    def post(self):
        try:
            data = UsuarioResource.parser.parse_args()
            if not data:
                return {"message": "Requisição sem JSON"}, 400

            if UsuarioModel.encontrar_pelo_nome(data['nome']):
                return {"message": "Usuário ja existe"}, 400
            else:
                usuario = UsuarioModel(data['nome'],
                                       data['tipoUsuario'],
                                       data['email'],
                                       data['senha'],
                                       data['cargo'],
                                       data['telefone'],
                                       data['foto'],
                                       data['avaliacao']
                                       )
                usuario.adicionar()
                usuario = UsuarioModel.encontrar_pelo_nome(data['nome'])

                user_schema = UsuarioSchema()
                json = user_schema.dump(usuario).data
                return json, 201

        except Exception as ex:
            print(ex)
            return {"message": "erro"}, 500

    def put(self):
        json = ''
        return json, 201

class UsuariosResource(Resource):
    def get(self):
        json = ""
        try:
            usuarios = UsuarioModel.listar()
            schema = UsuarioSchema(many=True)
            json = schema.dump(usuarios).data
        except Exception as e:
            print(e)
            return {"message": "Aconteceu um erro tentando retornar a lista de usuarios."}, 500
        return json, 200
