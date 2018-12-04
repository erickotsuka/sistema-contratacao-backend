from flask_restful import Resource, reqparse, abort
from flask import request
from toko.models.servico_model import ServicoModel
from toko.schemas.servico_schema import ServicoSchema

class ServicoResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("id_proposta",
                        type=int,
                        required=True,
                        help="O ID da proposta não pode estar em branco."
                        )
    parser.add_argument("titulo",
                        type=str,
                        required=True,
                        help="O titulo de Usuário não pode estar em branco."
                        )
    parser.add_argument('descricao',
                        type=str,
                        required=True,
                        help="A descricao do Servico não pode estar em branco."
                        )
    parser.add_argument('id_cronograma',
                        type=int,
                        required=True,
                        help="O cronograma do Servico não pode estar em branco."
                        )

    def get(self,titulo):
        json = ''
        try:
            servico = ServicoModel.encontrar_pelo_titulo(titulo)
            print(servico)
            if servico:
                schema = ServicoSchema()
                json = schema.dump(servico).data
            else:
                return {"message":"Servico {} não existe".format(titulo)},404
        except Exception as e:
            print(e)
            return {"message","Erro na requisição".format(titulo)},500

        return json,200

    def post(self):
        try:
            data = ServicoResource.parser.parse_args()
            if not data:
                return {"message": "Requisição sem JSON"}, 400

            if ServicoModel.encontrar_pelo_titulo(data['titulo']):
                return {"message": "Usuário ja existe"}, 400
            else:
                servico = ServicoModel(data['id_proposta'],
                                       data['titulo'],
                                       data['descricao'],
                                       data['id_cronograma'],
                                       )
                servico.adicionar()
                servico = ServicoModel.encontrar_pelo_titulo(data['titulo'])

                user_schema = ServicoSchema()
                json = user_schema.dump(servico).data
                return json, 201

        except Exception as ex:
            print(ex)
            return {"message": "erro"}, 500

    def put(self):
        json = ''
        return json, 201

class ServicosResource(Resource):
    def get(self):
        json = ""
        try:
            servicos = ServicoModel.listar()
            schema = ServicoSchema(many=True)
            json = schema.dump(servicos).data
        except Exception as e:
            print(e)
            return {"message": "Aconteceu um erro tentando retornar a lista de servicos."}, 500
        return json, 200
