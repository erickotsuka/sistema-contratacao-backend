from flask_restful import Resource, reqparse, abort
from flask import request
from toko.models.demanda_model import DemandaModel
from toko.schemas.demanda_schema import DemandaSchema

class DemandaResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("id_cliente",
                        type=int,
                        required=True,
                        help="O ID do cliente não pode estar em branco."
                        )
    parser.add_argument("titulo",
                        type=str,
                        required=True,
                        help="O título da demanda não pode estar em branco."
                        )
    parser.add_argument("data_limite",
                        type=lambda x: datetime.strptime(x,'%Y-%m-%dT%H:%M:%S'),
                        required=True,
                        help="Data limite da demanda não pode estar em branco."
                        )
    parser.add_argument('descricao',
                        type=str,
                        required=True,
                        help="A descrição da Demanda não pode estar em branco."
                        )

    def get(self,titulo):
        json = ''
        try:
            demanda = DemandaModel.encontrar_pelo_titulo(titulo)
            print(demanda)
            if demanda:
                schema = DemandaSchema()
                json = schema.dump(demanda).data
            else:
                return {"message":"Demanda {} não existe".format(titulo)},404
        except Exception as e:
            print(e)
            return {"message","Erro na requisição".format(titulo)},500

        return json,200

    def post(self):
        try:
            data = DemandaResource.parser.parse_args()
            if not data:
                return {"message": "Requisição sem JSON"}, 400

            if DemandaModel.encontrar_pelo_id(data['id']):
                return {"message": "ID da demanda ja existe"}, 400
            else:
                demanda = DemandaModel(data['id_cliente'],
                                       data['titulo'],
                                       data['data_limite'],
                                       data['descricao'],
                                       )
                demanda.adicionar()
                demanda = DemandaModel.encontrar_pelo_titulo(data['titulo'])

                user_schema = DemandaSchema()
                json = user_schema.dump(demanda).data
                return json, 201

        except Exception as ex:
            print(ex)
            return {"message": "erro"}, 500

    def put(self):
        json = ''
        return json, 201

class DemandasResource(Resource):
    def get(self):
        json = ""
        try:
            demandas = DemandaModel.listar()
            schema = DemandaSchema(many=True)
            json = schema.dump(demandas).data
        except Exception as e:
            print(e)
            return {"message": "Aconteceu um erro tentando retornar a lista de mensagens."}, 500
        return json, 200
