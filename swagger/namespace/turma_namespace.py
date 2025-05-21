from flask_restx import Namespace, Resource, fields
from turmas.turmas_repository import getTurma, getTurmasId, createTurma, updateTurmas, deleteTurmas, resetaAlunosProfessores

turmas_ns = Namespace("turma", description="Operações relacionadas às turmas")

turma_model = turmas_ns.model("Turma", {
    "descricao": fields.String(required=True, description="Descrição da Turma"),
    "ativo": fields.Boolean(required=True, description="Indica se a turma está ativa"),
    "professor_id": fields.Integer(required=True, description="ID do professor responsável")
})


turma_model_output = turmas_ns.model("TurmaOutput", {
    "turma_id": fields.Integer(description="ID da turma"),
    "descrição": fields.String(description="Descrição da Turma"),
    "ativo": fields.Boolean(description="Indica se a turma está ativa"),
    "professor_id": fields.Integer(description="ID do professor responsável")
})
@turmas_ns.route('/')
class TurmaResource(Resource):
    @turmas_ns.marshal_list_with(turma_model_output)
    def get(self):
        '''Listar todas as turmas'''
        return getTurma()
    
    @turmas_ns.expect(turma_model)
    def post(self):
        '''Criar uma nova turma'''
        dados = turmas_ns.payload
        resultado, status_code = createTurma(dados)
        return resultado, status_code

@turmas_ns.route('/<int:id_turma>')
class TurmaIdResource(Resource):
    @turmas_ns.marshal_with(turma_model_output)
    def get(self, id_turma):
        '''Obter uma turma pelo ID'''
        return getTurmasId(id_turma)
    
    @turmas_ns.expect(turma_model)
    def put(self, id_turma):
        '''Atualizar uma turma pelo ID'''
        dados = turmas_ns.payload
        updateTurmas(id_turma, dados)
        return dados, 200    
    
    def delete(self, id_turma):
        '''Excluir uma turma pelo ID'''
        deleteTurmas(id_turma)
        return {'mensagem': 'Turma apagada com sucesso!'}, 200