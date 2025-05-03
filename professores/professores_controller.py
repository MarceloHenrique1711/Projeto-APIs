from flask import request, jsonify
from .professores_model import Professor
from config import db


def getProfessores():
    professores = Professor.query.all()
    return jsonify([professor.to_dict() for professor in professores])

#verifica se o id passado existe em alguma turma
#no proprio endpoint da erro se nao for int "<int:idTurma">
def getProfessorId(idProfessor):
    professor = Professor.query.get(idProfessor)
    if not professor:
        return jsonify({'erro': 'Professor não encontrada'}), 404  
    return jsonify(professor.to_dict())

# criar um professor
def createProfessor():
    dados = request.json

    # Verifica se o nome está presente e não é vazio
    if "nome" not in dados or not isinstance(dados["nome"], str) or dados["nome"].strip() == "":
        return jsonify({"erro": "O campo 'nome' é obrigatório"}), 400

    # Verifica idade
    if "idade" not in dados or not isinstance(dados["idade"], int) or dados["idade"] < 0:
        return jsonify({"erro": "O campo 'idade' deve ser um número inteiro positivo"}), 400

    # Verifica matéria
    if "materia" not in dados or not isinstance(dados["materia"], str) or len(dados["materia"]) > 100:
        return jsonify({"erro": "O campo 'materia' tem que ser string e no máximo 100 caracteres"}), 400

    # Verifica observações (opcional)
    if "observacoes" in dados and not isinstance(dados["observacoes"], str):
        return jsonify({"erro": "O campo 'observacoes' deve ser uma string"}), 400

    # Cria o novo professor
    novo_professor = Professor(
        nome=dados["nome"],
        idade=dados["idade"],
        materia=dados["materia"],
        observacoes=dados.get("observacoes")  # opcional
    )

    db.session.add(novo_professor)
    db.session.commit()

    return jsonify({"mensagem": "Professor criado com sucesso!"}), 201

# atualizar um professor
def updateProfessor(idProfessor):
    professor = Professor.query.get(idProfessor)

    if not professor:
        return jsonify({"erro": "Professor não encontrado"}), 404

    dados = request.json

    # Validação do campo 'nome'
    if "nome" not in dados or not isinstance(dados["nome"], str) or dados["nome"].strip() == "":
        return jsonify({"erro": "O campo 'nome' é obrigatório e deve ser uma string válida"}), 400

    # Validação do campo 'idade'
    if "idade" not in dados or not isinstance(dados["idade"], int) or dados["idade"] < 0:
        return jsonify({"erro": "O campo 'idade' deve ser um número inteiro positivo"}), 400

    # Validação do campo 'materia'
    if "materia" not in dados or not isinstance(dados["materia"], str) or len(dados["materia"]) > 100:
        return jsonify({"erro": "O campo 'materia' deve ser uma string com no máximo 100 caracteres"}), 400

    # Validação do campo 'observacoes'
    if "observacoes" in dados and not isinstance(dados["observacoes"], str):
        return jsonify({"erro": "O campo 'observacoes' deve ser uma string"}), 400

    # Atualização dos dados
    if "nome" in dados and isinstance(dados["nome"], str) and dados["nome"].strip() != "":
      professor.nome = dados["nome"]
    if "idade" in dados and isinstance(dados["idade"], int) and dados["idade"] >= 0:
      professor.idade = dados["idade"]
    if "materia" in dados and isinstance(dados["materia"], str) and len(dados["materia"]) <= 100:
      professor.materia = dados["materia"]
    if "observacoes" in dados and isinstance(dados["observacoes"], str):
      professor.observacoes = dados["observacoes"]  # pode ser None ou uma string válida  

    db.session.commit()

    return jsonify({
        "mensagem": "Professor atualizado com sucesso!"}), 200

# deletar um professor
def deleteProfessor(idProfessor):
    professor = Professor.query.get(idProfessor)
    if not professor:
        return jsonify({'erro': 'Professor não encontrada'}), 404  
    db.session.delete(professor)
    db.session.commit()
    return jsonify({'mensagem': 'Professor apagado com sucesso!'}), 200

