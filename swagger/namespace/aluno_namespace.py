from flask_restx import Namespace, Resource, fields
from alunos.alunos_controller import getAluno, getAlunosId, createAluno, updateAlunos, deleteAlunos

alunos_ns = Namespace("Aluno", description="Operações relacionadas aos alunos")

aluno_model = alunos_ns.model("Aluno", {
    "nome": fields.String(required=True, description="Nome do aluno"),
    "data_de_nascimento": fields.String(required=True, description="Data de nascimento (dd-mm-aaaa)"),
    "nota_primeiro_semestre": fields.Float(required=True, description="Nota do primeiro semestre"),
    "nota_segundo_semestre": fields.Float(required=True, description="Nota do segundo semestre"),
    "turma_id": fields.Integer(required=True, description="ID da turma associada"),
})

aluno_output_model = alunos_ns.model("AlunoOutput", {
    "id": fields.Integer(description="ID do aluno"),
    "nome": fields.String(required=True, description="Nome do aluno"),
    "idade": fields.Integer(required=True, description="Idade do aluno"),
    "data_de_nascimento": fields.String(required=True, description="Data de nascimento (YYYY-MM-DD)"),
    "nota_primeiro_semestre": fields.Float(required=True, description="Nota do primeiro semestre"),
    "nota_segundo_semestre": fields.Float(required=True, description="Nota do segundo semestre"),
    "media_final": fields.Float(required=True, description="Média final do aluno"),
    "turma_id": fields.Integer(required=True, description="ID da turma associada"),
})

erro_model = alunos_ns.model("Erro", {
    "erro": fields.String(example="Aluno não encontrado")
})

@alunos_ns.route("/")
class AlunosResource(Resource):
    @alunos_ns.marshal_list_with(aluno_output_model)
    def get(self):
        """Lista todos os alunos"""
        return getAluno()

    @alunos_ns.expect(aluno_model)
    @alunos_ns.response(201, "Aluno criado com sucesso", aluno_output_model)
    @alunos_ns.response(400, "Dados inválidos", model=erro_model)
    def post(self):
        """Cria um novo aluno"""
        dados = alunos_ns.payload
        resultado, status_code = createAluno(dados) #estava assim antes createAluno(dados)
        return resultado, status_code

@alunos_ns.route("/<int:id_aluno>")
class AlunoIdResource(Resource):
    @alunos_ns.response(200, "Aluno encontrado", aluno_output_model)
    @alunos_ns.response(404, "Aluno não encontrado", erro_model)
    def get(self, id_aluno):
        """Obtém um aluno pelo ID"""
        resultado, status_code = getAlunosId(id_aluno)
        return resultado, status_code

    @alunos_ns.expect(aluno_model)
    @alunos_ns.response(400, "Dados inválidos", model=erro_model)
    @alunos_ns.response(404, "Aluno não encontrado", model=erro_model)
    def put(self, id_aluno):
        """Atualiza um aluno pelo ID"""
        dados = alunos_ns.payload
        resposta, status_code = updateAlunos(id_aluno, dados)
        return resposta, status_code

    @alunos_ns.response(404, "Aluno não encontrado", model=erro_model)
    def delete(self, id_aluno):
        """Exclui um aluno pelo ID"""
        resultado, status_code = deleteAlunos(id_aluno)
        return resultado, status_code