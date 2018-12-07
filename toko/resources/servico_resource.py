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

    def get(self,id):
        json = ''
        try:
            servico = ServicoModel.encontrar_pelo_id(id)
            print(servico)
            if servico:
                schema = ServicoSchema()
                json = schema.dump(servico).data
            else:
                return {"message":"Servico {} não existe".format(id)},404
        except Exception as e:
            print(e)
            return {"message","Erro na requisição".format(id)},500

        return json,200

    def delete(self,id):
        json = []
        try:
            servico = ServicoModel.encontrar_pelo_id(id)
            if servico:
                servico.remover()
                lista = ServicoModel.listar()
                schema = ServicoSchema(many=True,exclude=['listas'])
                json = schema.dump(lista).data
            else:
                return {"message":"Servico {} não está na lista".format(id)},404
        except Exception as e:
            print(e)
        return json, 201

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
        try:
            data = ServicoResource.parser.parse_args()
            id_proposta = data['id_proposta']
            titulo = data['titulo']
            descricao = data['descricao']
            id_cronograma = data['id_cronograma']

            servico = ServicoModel.encontrar_pelo_titulo(titulo)
            if servico:
                return {"message":"Servico {} já está na lista".format(servico.titulo)},200
            else:
                servico = ServicoModel(
                    id_proposta=id_proposta,
                    titulo=titulo,
                    descricao=descricao,
                    id_cronograma=id_cronograma
                )
                servico.adicionar()
                schema = ServicoSchema(many=False)
                servico = ServicoModel.encontrar_pelo_titulo(titulo)
                json = schema.dump(servico).data
        except Exception as e:
            print(e)
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
