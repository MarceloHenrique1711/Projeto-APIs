from flask import Blueprint
from .turmas_repository import *

turma_blueprint = Blueprint('turmas', __name__,url_prefix='/turmas')
reseta_blueprint = Blueprint('reseta', __name__,url_prefix='/reseta')
resetaTurma_blueprint = Blueprint('resetaTurma', __name__,url_prefix='/resetaTurma')


@turma_blueprint.route("/", methods=['GET'])
def listar_turmas():
    return getTurma()

@turma_blueprint.route('/por_sala/<int:sala_id>', methods=['GET'])
def listar_sala_por_id(sala_id):
    return get_turma_por_sala(sala_id)

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

@resetaTurma_blueprint.route("/", methods=["POST", 'DELETE'])
def resetar_turma():
    return resetaTurmas()

@reseta_blueprint.route('/', methods=["POST",'DELETE'])
def resetar_dados():
    return resetaAlunosProfessores()