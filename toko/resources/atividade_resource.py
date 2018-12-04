from flask_restful import Resource, reqparse, abort
from flask import request
from toko.models.atividade_model import AtividadeModel
from toko.schemas.atividade_schema import AtividadeSchema

class AtividadeResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("id_cronograma",
                        type=int,
                        required=True,
                        help="O ID do cronograma não pode estar em branco."
                        )
    parser.add_argument("nome",
                        type=str,
                        required=True,
                        help="O nome da atividade não pode estar em branco."
                        )
    parser.add_argument("entrega",
                        type=lambda x: datetime.strptime(x,'%Y-%m-%dT%H:%M:%S'),
                        required=True,
                        help="A entrega da atividade não pode estar em branco."
                        )
    parser.add_argument('descricao',
                        type=str,
                        required=True,
                        help="A descrição da Atividade não pode estar em branco."
                        )

    def get(self,id):
        json = ''
        try:
            atividade = AtividadeModel.encontrar_pelo_id(id)
            print(atividade)
            if atividade:
                schema = AtividadeSchema()
                json = schema.dump(atividade).data
            else:
                return {"message":"Atividade {} não existe".format(id)},404
        except Exception as e:
            print(e)
            return {"message","Erro na requisição".format(id)},500

        return json,200

    def post(self):
        try:
            data = AtividadeResource.parser.parse_args()
            if not data:
                return {"message": "Requisição sem JSON"}, 400

            if AtividadeModel.encontrar_pelo_id(data['id']):
                return {"message": "ID da atividade ja existe"}, 400
            else:
                atividade = AtividadeModel(data['id_cronograma'],
                                       data['nome'],
                                       data['entrega'],
                                       data['descricao'],
                                       )
                atividade.adicionar()
                atividade = AtividadeModel.encontrar_pelo_id(data['id'])

                user_schema = AtividadeSchema()
                json = user_schema.dump(atividade).data
                return json, 201

        except Exception as ex:
            print(ex)
            return {"message": "erro"}, 500

    def put(self):
        json = ''
        return json, 201

class AtividadesResource(Resource):
    def get(self):
        json = ""
        try:
            atividades = AtividadeModel.listar()
            schema = AtividadeSchema(many=True)
            json = schema.dump(atividades).data
        except Exception as e:
            print(e)
            return {"message": "Aconteceu um erro tentando retornar a lista de mensagens."}, 500
        return json, 200
