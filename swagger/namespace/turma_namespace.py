from flask_restx import Namespace, Resource, fields
from turmas.turmas_controller import getTurma, getTurmasId, createTurma, updateTurmas, deleteTurmas, resetaAlunosProfessores

turmas_ns = Namespace("Turma", description="Operações relacionadas às turmas")

turma_model = turmas_ns.model("Turma", {
    "descricao": fields.String(required=True, description="Descrição da Turma"),
    "ativo": fields.String(required=True, description="Indica se a turma está ativa"),
    "professor_id": fields.Integer(required=True, description="ID do professor responsável")
})


turma_model_output = turmas_ns.model("TurmaOutput", {
    "turma_id": fields.Integer(description="ID da turma"),
    "Descrição": fields.String(required=True, description="Descrição da Turma"),
    "Ativo": fields.String(required=True, description="Indica se a turma está ativa"),
    "professor_id": fields.Integer(required=True, description="ID do professor responsável")
})

erro_model = turmas_ns.model("Erro", {
    "erro": fields.String(example="Turma não encontrada")
})

@turmas_ns.route('/')
class TurmaResource(Resource):
    @turmas_ns.marshal_list_with(turma_model_output)
    def get(self):
        '''Listar todas as turmas'''
        return getTurma()
    
    @turmas_ns.expect(turma_model)
    @turmas_ns.response(201, "Turma criada com sucesso", model=turma_model_output)
    @turmas_ns.response(400, "Dados inválidos", model=erro_model)
    
    def post(self):
        '''Criar uma nova turma'''
        dados = turmas_ns.payload
        resultado, status_code = createTurma(dados)
        return resultado, status_code

@turmas_ns.route('/<int:id_turma>')
class TurmaIdResource(Resource):
    @turmas_ns.response(200, "Turma encontrada", model=turma_model_output)
    @turmas_ns.response(404, "Turma não encontrada", model=erro_model)
    def get(self, id_turma):
        '''Obter uma turma pelo ID'''
        resultado, status_code = getTurmasId(id_turma)
        return resultado, status_code
    
    @turmas_ns.expect(turma_model)
    @turmas_ns.response(400, "Dados inválidos", erro_model)
    @turmas_ns.response(404, "Turma não encontrada", model=erro_model)
    
    def put(self, id_turma):
        '''Atualizar uma turma pelo ID'''
        dados = turmas_ns.payload
        resultado, status_code = updateTurmas(id_turma, dados)
        return resultado, status_code
    
    @turmas_ns.response(404, "Turma não encontrada", model=erro_model)
    def delete(self, id_turma):
        '''Excluir uma turma pelo ID'''
        resultado, status_code = deleteTurmas(id_turma)
        return resultado, status_code