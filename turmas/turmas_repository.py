from flask import request, jsonify
import requests
from .turmas_model import Turma
from config import db
from professores.professores_model import Professor
from alunos.alunos_model import Aluno

def getTurma():
    turmas = Turma.query.all()
    return jsonify([turma.to_dict() for turma in turmas])

def getTurmasId(idTurma):
    
    turma = Turma.query.get(idTurma)
    if not turma:
        return jsonify({'erro': 'Turma não encontrada'}), 404  
    return jsonify(turma.to_dict()), 200

def validar_dados_turma(dados, update=False):
    # Verifica se descricao é string
    if not isinstance(dados.get('descricao'), str):
        return False, {"erro": "Descricao deve ser uma string"}

    # Verifica tamanho máximo da descrição
    if len(dados['descricao']) > 100:
        return False, {"erro": "Descricao deve ter no máximo 100 caracteres"}

    if 'professor_id' in dados:
      if not isinstance(dados['professor_id'], int):
        return False, {"erro": "professor_id deve ser um número inteiro"}
    
    # Se for criação ou atualização do campo professor_id, verifica existência no banco
      if not update or (update and 'professor_id' in dados):
          # importe local para evitar circularidade
        if not Professor.query.get(dados['professor_id']):
            return False, {"erro": "Professor inexistente"}

    # Verifica se ativo é booleano
    if not isinstance(dados.get('ativo'), bool):
        return False, {"erro": "Ativo deve ser True ou False"}

    return True, None


def createTurma():
    dados = request.json

    # Valida os dados da turma
    is_valid, error = validar_dados_turma(dados)
    if not is_valid:
        return jsonify(error), 400

    professor = Professor.query.get(dados['professor_id'])
    if not professor:
        return jsonify({"erro": "Professor não encontrado"}), 400
    
    try:
        # Requisição à API A para obter sala disponível
        resposta = requests.get("http://api_sala:6000/salas/disponivel")
        
        if resposta.status_code == 404:
            return jsonify({"erro": "Nenhuma sala disponível no momento"}), 400

        sala = resposta.json()
        sala_id = sala['sala_id']

        # Cria a nova turma
        nova_turma = Turma(
            descricao=dados['descricao'],
            professor_id=dados['professor_id'],
            ativo=dados['ativo'],
            sala_id=sala_id
        )
        db.session.add(nova_turma)
        db.session.commit()

        return jsonify({'mensagem': 'Turma criada com sucesso!'}), 201
    except Exception as e:
        return jsonify({"erro": f"Erro ao criar turma: {str(e)}"}), 500


def updateTurmas(idTurma):
    turma = Turma.query.get(idTurma)

    if not turma:
        return jsonify({"erro": "Turma não encontrada"}), 404

    dados = request.json

    # Valida os dados da turma
    is_valid, error = validar_dados_turma(dados, update=True)
    if not is_valid:
        return jsonify(error), 400

    # Atualiza os campos da turma
    if 'descricao' in dados:
        turma.descricao = dados['descricao']
    if 'professor_id' in dados:
        turma.professor_id = dados['professor_id']
    if 'ativo' in dados:
        turma.ativo = dados['ativo']

    db.session.commit()

    return jsonify({"mensagem": "Turma atualizada com sucesso!"}), 200


def deleteTurmas(idTurma):
    turma = Turma.query.get(idTurma)
    if not turma:
        return jsonify({'erro': 'Turma não encontrada'}), 404  
    try:
        db.session.delete(turma)
        db.session.commit()
        return jsonify({'mensagem': 'Turma apagada com sucesso!'}), 200
    except Exception as e:
        return jsonify({"erro": f"Erro ao tentar apagar a turma: {str(e)}"}), 500

def resetaAlunosProfessores():
    
    try:
        db.session.query(Professor).delete()
        db.session.query(Aluno).delete()  
        db.session.commit()
        return jsonify({'mensagem': 'Alunos e professores foram apagados com sucesso!'}), 200
    except Exception as e:
        return jsonify({"erro": f"Erro ao tentar resetar os dados: {str(e)}"}), 404

#metodo só para os testes de turma 
def resetaTurmas():
    
    try:
        db.session.query(Turma).delete()
        db.session.commit()
        return jsonify({'mensagem': 'Todas as turmas foram apagados com sucesso!'}), 200
    except Exception as e:
        return jsonify({"erro": f"Erro ao tentar resetar os dados: {str(e)}"}), 404


def get_turma_por_sala(sala_id):
    turma = Turma.query.filter_by(sala_id=sala_id).first()
    if turma:
        return jsonify(turma.to_dict()), 200
    else:
        return jsonify({}), 200  # Retorna 200 com objeto vazio se nenhuma turma usar a sala