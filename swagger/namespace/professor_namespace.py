from flask_restx import Namespace, Resource, fields
from professores.professores_repository import getProfessores, getProfessorId, createProfessor, updateProfessor, deleteProfessor

professores_ns = Namespace("Professor", description="Operações relacionadas aos professores")

professor_model = professores_ns.model("Professor", {  # Corrigido de "Aluno" para "Professor"
    "nome": fields.String(required=True, description="Nome do professor"),
    "idade": fields.Integer(required=True, description="Idade do professor"),
    "materia": fields.String(required=False, description="Matéria do professor"),
    "observacoes": fields.String(description="Observação do professor"),
})

professor_output_model = professores_ns.model("ProfessorOutput", {
    "id": fields.Integer(description="ID do professor"),
    "nome": fields.String(description="Nome do professor"),
    "idade": fields.Integer(description="Idade do professor"),
    "materia": fields.String(description="Matéria do professor"),
    "observacoes": fields.String(description="Observação do professor"),
})

@professores_ns.route("/")
class ProfessoresResource(Resource):
    @professores_ns.marshal_list_with(professor_output_model)
    def get(self):
        """Lista todos os professores"""
        return getProfessores()

    @professores_ns.expect(professor_model)
    def post(self):
        """Cria um novo professor"""
        dados = professores_ns.payload
        resultado, status_code = createProfessor(dados)  # Removido o argumento 'data'
        return resultado, status_code

@professores_ns.route("/<int:id_professor>")  # Corrigido de 'id_aluno' para 'id_professor'
class ProfessorIdResource(Resource):
    @professores_ns.marshal_with(professor_output_model)
    def get(self, id_professor):  # Corrigido de 'id_aluno' para 'id_professor'
        """Obtém um professor pelo ID"""
        return getProfessorId(id_professor)

    @professores_ns.expect(professor_model)
    def put(self, id_professor):
        """Atualiza um professor pelo ID"""
        dados = professores_ns.payload
        professor_atualizado = updateProfessor(id_professor, dados)  # Removido o argumento 'data'
        return professor_atualizado, 200

    def delete(self, id_professor):
        """Exclui um professor pelo ID"""  # Corrigido de "aluno" para "professor"
        deleteProfessor(id_professor)
        return {"message": "Professor excluído com sucesso"}, 200  # Corrigido de "Aluno" para "Professor"