from flask_restful import Resource, reqparse, abort
from flask import request
from toko.models.proposta_model import PropostaModel
from toko.schemas.proposta_schema import PropostaSchema
from datetime import datetime

class PropostaResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("id_demanda",
                        type=int,
                        required=True,
                        help="O ID da proposta não pode estar em branco."
                        )
    parser.add_argument("prazo",
                        type=lambda x: datetime.strptime(x,'%Y-%m-%dT%H:%M:%S'),
                        required=True,
                        help="O prazo não pode estar em branco."
                        )
    parser.add_argument('orcamento',
                        type=float,
                        required=True,
                        help="O orçamento da Proposta não pode estar em branco."
                        )
    parser.add_argument('id_integrador',
                        type=int,
                        required=True,
                        help="O ID do integrador da proposta não pode estar em branco."
                        )
    parser.add_argument('titulo',
                        type=str,
                        required=True,
                        help="O título da Proposta não pode estar em branco."
                        )
    parser.add_argument('descricao',
                        type=str,
                        required=True,
                        help="A descricao da Proposta não pode estar em branco."
                        )
    parser.add_argument('status',
                        type=str,
                        required=True,
                        help="O status da Proposta não pode estar em branco."
                        )

    def get(self,titulo):
        json = ''
        try:
            proposta = PropostaModel.encontrar_pelo_titulo(titulo)
            print(proposta)
            if proposta:
                schema = PropostaSchema()
                json = schema.dump(proposta).data
            else:
                return {"message":"Proposta {} não existe".format(titulo)},404
        except Exception as e:
            print(e)
            return {"message","Erro na requisição".format(titulo)},500

        return json,200

    def delete(self,titulo):
        json = []
        try:
            proposta = PropostaModel.encontrar_pelo_titulo(tiulo)
            if proposta:
                proposta.remover()
                lista = PropostaModel.listar()
                schema = PropostaSchema(many=True,exclude=['listas'])
                json = schema.dump(lista).data
            else:
                return {"message":"Proposta {} não está na lista".format(nome)},404
        except Exception as e:
            print(e)
        return json, 201


    def post(self):
        try:
            data = PropostaResource.parser.parse_args()
            if not data:
                return {"message": "Requisição sem JSON"}, 400

            if PropostaModel.encontrar_pelo_titulo(data['titulo']):
                return {"message": "Usuário ja existe"}, 400
            else:
                proposta = PropostaModel(data['id_demanda'],
                                       data['prazo'],
                                       data['orcamento'],
                                       data['id_integrador'],
                                       data['titulo'],
                                       data['descricao'],
                                       data['status'],
                                       )
                proposta.adicionar()
                proposta = PropostaModel.encontrar_pelo_titulo(data['titulo'])

                user_schema = PropostaSchema()
                json = user_schema.dump(proposta).data
                return json, 201

        except Exception as ex:
            print(ex)
            return {"message": "erro"}, 500

    def put(self):
        json = ''
        try:
            data = PropostaResource.parser.parse_args()
            id_demanda = data['id_demanda']
            prazo = data['prazo']
            orcamento = data['orcamento']
            id_integrador = data['id_integrador']
            titulo = data['titulo']
            descricao = data['descricao']
            status = data['status']

            proposta = PropostaModel.encontrar_pelo_titulo(titulo)
            if proposta:
                return {"message":"Proposta {} já está na lista".format(proposta.titulo)},200
            else:
                proposta = PropostaModel(
                    id_demanda=id_demanda,
                    prazo=prazo,
                    orcamento=orcamento,
                    id_integrador=id_integrador,
                    titulo=titulo,
                    descricao=descricao,
                    status=status
                )
                proposta.adicionar()
                schema = PropostaSchema(many=True)
                proposta = PropostaModel.encontrar_pelo_titulo(titulo)
                json = schema.dump(proposta).data
        except Exception as e:
            print(e)
        return json, 201

class PropostasResource(Resource):
    def get(self):
        json = ""
        try:
            propostas = PropostaModel.listar()
            schema = PropostaSchema(many=True)
            json = schema.dump(propostas).data
        except Exception as e:
            print(e)
            return {"message": "Aconteceu um erro tentando retornar a lista de propostas."}, 500
        return json, 200
