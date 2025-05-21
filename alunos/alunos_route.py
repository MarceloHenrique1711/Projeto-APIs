from flask import Blueprint
from .alunos_repository import *


alunos_blueprint = Blueprint('alunos', __name__,url_prefix='/alunos')


@alunos_blueprint.route("/", methods=['GET'])
def listar_alunos():
    return getAluno()

@alunos_blueprint.route('/<int:idAluno>', methods=['GET'])
def listar_aluno_por_id(idAluno):
    return getAlunosId(idAluno)

@alunos_blueprint.route('/', methods=['POST'])
def criar_aluno():
    return createAluno()

@alunos_blueprint.route('/<int:idAluno>', methods=['PUT'])
def atualizar_aluno(idAluno):
    return updateAlunos(idAluno)

@alunos_blueprint.route('/<int:idAluno>', methods=['DELETE'])
def deletar_aluno(idAluno):
    return deleteAlunos(idAluno)