from flask import Blueprint
from .turmas_model import *


turma_blueprint = Blueprint('turmas', __name__,url_prefix='/turmas')
reseta_blueprint = Blueprint('reseta', __name__,url_prefix='/reseta')


@turma_blueprint.route("/", methods=['GET'])
def listar_turmas():
    return getTurma()

@turma_blueprint.route('/<int:idTurma>', methods=['GET'])
def listar_turma_por_id(idTurma):
    return getTurmasId(idTurma)

@turma_blueprint.route('/', methods=['POST'])
def criar_turma():
    return createTurma()

@turma_blueprint.route('/<int:idTurma>', methods=['PUT'])
def atualizar_turma(idTurma):
    return updateTurmas(idTurma)

@turma_blueprint.route('/<int:idTurma>', methods=['DELETE'])
def deletar_turma(idTurma):
    return deleteTurmas(idTurma)

@reseta_blueprint.route('/', methods=["POST",'DELETE'])
def resetar_dados():
    return resetaAlunosProfessores()