from flask_restful import Resource, reqparse, abort
from flask import request
from toko.models.mensagem_model import MensagemModel
from toko.schemas.mensagem_schema import MensagemSchema
from datetime import datetime

class MensagemResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("id_chat",
                        type=int,
                        required=True,
                        help="O ID do chat não pode estar em branco."
                        )
    parser.add_argument("id_usuario_de",
                        type=int,
                        required=True,
                        help="O ID do usuário de origem não pode estar em branco."
                        )
    parser.add_argument("id_usuario_para",
                        type=int,
                        required=True,
                        help="O ID do usuário de destino não pode estar em branco."
                        )
    parser.add_argument("data_hora",
                        type=lambda x: datetime.strptime(x,'%Y-%m-%dT%H:%M:%S'),
                        required=True,
                        help="Data e hora da mensagem não pode estar em branco."
                        )
    parser.add_argument('conteudo',
                        type=str,
                        required=True,
                        help="O conteúdo da Mensagem não pode estar em branco."
                        )

    def get(self,id):
        json = ''
        try:
            mensagem = MensagemModel.encontrar_pelo_id(id)
            print(mensagem)
            if mensagem:
                schema = MensagemSchema()
                json = schema.dump(mensagem).data
            else:
                return {"message":"Mensagem {} não existe".format(id)},404
        except Exception as e:
            print(e)
            return {"message","Erro na requisição".format(id)},500

        return json,200

    def delete(self,id):
        json = []
        try:
            mensagem = MensagemModel.encontrar_pelo_id(id)
            if mensagem:
                mensagem.remover()
                lista = MensagemModel.listar()
                schema = MensagemSchema(many=True,exclude=['listas'])
                json = schema.dump(lista).data
            else:
                return {"message":"Mensagem {} não está na lista".format(id)},404
        except Exception as e:
            print(e)
        return json, 201


    def post(self):
        try:
            data = MensagemResource.parser.parse_args()
            if not data:
                return {"message": "Requisição sem JSON"}, 400

            if MensagemModel.encontrar_pelo_id(data['id']):
                return {"message": "ID da mensagem ja existe"}, 400
            else:
                mensagem = MensagemModel(data['id_chat'],
                                       data['id_usuario_de'],
                                       data['id_usuario_para'],
                                       data['data_hora'],
                                       data['conteudo'],
                                       )
                mensagem.adicionar()
                mensagem = MensagemModel.encontrar_pelo_id_chat(data['id_chat'])

                user_schema = MensagemSchema()
                json = user_schema.dump(mensagem).data
                return json, 201

        except Exception as ex:
            print(ex)
            return {"message": "erro"}, 500

    def put(self):
        json = ''
        try:
            data = MensagemResource.parser.parse_args()
            id_chat = data['id_chat']
            id_usuario_de = data['id_usuario_de']
            id_usuario_para = data['id_usuario_para']
            data_hora = data['data_hora']
            conteudo = data['conteudo']

            mensagem = MensagemModel(
                id_chat=id_chat,
                id_usuario_de=id_usuario_de,
                id_usuario_para=id_usuario_para,
                data_hora=data_hora,
                conteudo=conteudo
            )
            mensagem.adicionar()
            schema = MensagemSchema(many=True)
            # mensagem = MensagemModel.encontrar_pelo_id(id)
            json = schema.dump(mensagem).data
        except Exception as e:
            print(e)
        return json, 201

class MensagensResource(Resource):
    def get(self):
        json = ""
        try:
            mensagems = MensagemModel.listar()
            schema = MensagemSchema(many=True)
            json = schema.dump(mensagems).data
        except Exception as e:
            print(e)
            return {"message": "Aconteceu um erro tentando retornar a lista de mensagens."}, 500
        return json, 200
