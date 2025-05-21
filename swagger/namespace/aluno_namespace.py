from flask_restx import Namespace, Resource, fields
from alunos.alunos_repository import getAluno, getAlunosId, createAluno, updateAlunos, deleteAlunos



alunos_ns = Namespace("Aluno", description="Operações relacionadas aos alunos")

aluno_model = alunos_ns.model("Aluno", {
    "nome": fields.String(required=True, description="Nome do aluno"),
    "data_de_nascimento": fields.String(required=True, description="Data de nascimento (dd-mm-aaaa)"),
    "nota_primeiro_semestre": fields.Float(required=False, description="Nota do primeiro semestre"),
    "nota_segundo_semestre": fields.Float(required=False, description="Nota do segundo semestre"),
    "turma_id": fields.Integer(required=True, description="ID da turma associada"),
})

aluno_output_model = alunos_ns.model("AlunoOutput", {
    "id": fields.Integer(description="ID do aluno"),
    "nome": fields.String(required=True, description="Nome do aluno"),
    "idade": fields.Integer(required=True, description="Idade do aluno"),
    "data_de_nascimento": fields.String(required=True, description="Data de nascimento (dd-mm-aaaa)"),
    "nota_primeiro_semestre": fields.Float(required=False, description="Nota do primeiro semestre"),
    "nota_segundo_semestre": fields.Float(required=False, description="Nota do segundo semestre"),
    "media_final": fields.Float(required=False, description="Média final do aluno"),
    "turma_id": fields.Integer(required=True, description="ID da turma associada"),
})

@alunos_ns.route("/")
class AlunosResource(Resource):
    @alunos_ns.marshal_list_with(aluno_output_model)
    def get(self):
        """Lista todos os alunos"""
        return getAluno()

    @alunos_ns.expect(aluno_model)
    def post(self):
        """Cria um novo aluno"""
        dados = alunos_ns.payload
        resultado, status_code = createAluno(dados) #estava assim antes createAluno(dados)
        return resultado, status_code

@alunos_ns.route("/<int:id_aluno>")
class AlunoIdResource(Resource):
    @alunos_ns.marshal_with(aluno_output_model)
    def get(self, id_aluno):
        """Obtém um aluno pelo ID"""
        return getAlunosId(id_aluno)
    
    @alunos_ns.expect(aluno_model)
    @alunos_ns.marshal_with(aluno_output_model)
    def put(self, id_aluno):
        """Atualiza um aluno pelo ID (todos os campos obrigatórios)"""
        dados = alunos_ns.payload
        aluno_atualizado = updateAlunos(id_aluno, dados)
        return aluno_atualizado, 200

    def delete(self, id_aluno):
        """Exclui um aluno pelo ID"""
        deleteAlunos(id_aluno)
        return {'mensagem': 'Aluno apagado com sucesso!'}, 200