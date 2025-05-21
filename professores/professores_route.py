from flask import Blueprint
from .professores_repository import *


professor_blueprint = Blueprint('professores', __name__, url_prefix='/professores')


@professor_blueprint.route("/", methods=['GET'])
def listar_professores():
    return getProfessores()

@professor_blueprint.route('/<int:idProfessor>', methods=['GET'])
def listar_professor_por_id(idProfessor):
    return getProfessorId(idProfessor)

@professor_blueprint.route('/', methods=['POST'])
def criar_professor():
    return createProfessor()

@professor_blueprint.route('/<int:idProfessor>', methods=['PUT'])
def atualizar_professor(idProfessor):
    return updateProfessor(idProfessor)

@professor_blueprint.route('/<int:idProfessor>', methods=['DELETE'])
def deletar_professor(idProfessor):
    return deleteProfessor(idProfessor)