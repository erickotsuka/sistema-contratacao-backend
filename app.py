from flask import Flask
from flask_cors import CORS
from flask_restful import Api
#Importar cada recurso usado pela API.
from toko.resources.atividade_resource import AtividadeResource, AtividadesResource
from toko.resources.demanda_resource import DemandaResource,DemandasResource
from toko.resources.mensagem_resource import MensagemResource, MensagensResource
from toko.resources.proposta_resource import PropostaResource, PropostasResource
from toko.resources.servico_resource import ServicoResource, ServicosResource
from toko.resources.usuario_resource import UsuarioResource, UsuariosResource

app = Flask(__name__)
#Configuracoes relativas ao sqlalchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SQLALCHEMY_ECHO'] = True

app.secret_key = b'\xc4]gW\x0f\x8d\xc8\x05ocG\xf1\xb1j,{'

#fim configuracoes relativas ao sqlalchemy
api = Api(app)
CORS(app,resources={r"/*": {"origins": "*"}}) #O uso do cors
#cria as tabelas do banco de dados, caso elas nao estejam criadas
@app.before_first_request
def create_tables():
    print("criar tabelas")
    db.create_all()
#fim criacao de tabelas

api.add_resource(AtividadesResource, '/atividades')
api.add_resource(AtividadeResource, '/atividade', '/atividade/<int:id>')

api.add_resource(DemandasResource, '/demandas')
api.add_resource(DemandaResource, '/demanda','/demanda/<int:id>')

api.add_resource(MensagensResource, '/mensagens')
api.add_resource(MensagemResource, '/mensagem','/mensagem/<int:id>')

api.add_resource(PropostasResource, '/propostas')
api.add_resource(PropostaResource, '/proposta','/proposta/<int:id>')

api.add_resource(ServicosResource, '/servicos')
api.add_resource(ServicoResource, '/servico','/servico/<int:id>')

api.add_resource(UsuariosResource, '/usuarios')
api.add_resource(UsuarioResource,'/usuario','/usuario/<int:id>')

if __name__ == '__main__':
    from dao import db
    db.init_app(app)
    app.run(port=5000,debug=True)
