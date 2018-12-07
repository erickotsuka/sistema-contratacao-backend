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

    def delete(self,id_cronograma,nome):
        json = []
        try:
            atividade = AtividadeModel.encontrar_pelo_cronograma_e_nome(id_cronograma, nome)
            if atividade:
                atividade.remover()
                lista = AtividadeModel.listar()
                schema = AtividadeSchema(many=True,exclude=['listas'])
                json = schema.dump(lista).data
            else:
                return {"message":"Atividade {} não está na lista".format(nome)},404
        except Exception as e:
            print(e)
        return json, 201

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
        try:
            data = AtividadeResource.parser.parse_args()
            id_cronograma = data['id_cronograma']
            nome = data['nome']
            entrega = data['entrega']
            descricao = data['descricao']

            atividade = AtividadeModel.encontrar_pelo_cronograma_e_nome(id_cronograma, nome)
            if atividade:
                return {"message":"Atividade {} já está na lista".format(atividade.nome)},200
            else:
                atividade = AtividadeModel(
                    id_cronograma=id_cronograma,
                    nome=nome,
                    entrega=entrega,
                    descricao=descricao
                )
                atividade.adicionar()
                schema = AtividadeSchema(many=True)
                atividade = AtividadeModel.encontrar_pelo_cronograma_e_nome(id_cronograma, nome)
                json = schema.dump(atividade).data
        except Exception as e:
            print(e)
        return json, 201

class AtividadesResource(Resource):
    def get(self, id_cronograma):
        json = ""
        try:
            atividades = AtividadeModel.listar_pelo_id_cronograma(id_cronograma)
            schema = AtividadeSchema(many=True)
            json = schema.dump(atividades).data
        except Exception as e:
            print(e)
            return {"message": "Aconteceu um erro tentando retornar a lista de mensagens."}, 500
        return json, 200
