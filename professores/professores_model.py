from flask import jsonify, request
from dicionario import *


# professores
def getProfessores():
    return jsonify(dici["professor"])

#verifica se o id passado existe em alguma turma
#no proprio endpoint da erro se nao for int "<int:idTurma">
def getProfessorId(idProfessor):
    professores = dici["professor"]
    for professor in professores:
        if professor['id'] == idProfessor:
            dados = professor
            return jsonify(dados)
    return jsonify({"erro ": "Não existe esse professor"}), 404

# criar um professor
def createProfessor():
    dados = request.json

    #Verifica se o ID não está vazio
    if "id" not in dados or dados["id"] == "":
        return jsonify({"erro": "O campo 'id' é obrigatório"}), 400

    #Verifica se o ID é um número inteiro e se não é negativo
    if not isinstance(dados["id"], int) or dados["id"] < 0:
        return jsonify({"erro": "O campo 'id' deve ser um número inteiro positivo"}), 400

    #Verifica se já existe um professor com esse ID
    if any(prof["id"] == dados["id"] for prof in dici["professor"]):
        return jsonify({"erro": "Esse ID já está sendo utilizado"}), 400

    #Verifica se o NOME não está vazio
    if "nome" not in dados or dados["nome"].strip() == "":
        return jsonify({"erro": "O campo 'nome' é obrigatório"}), 400

    #Verifica se a idade foi fornecida, se é um número inteiro e se não é negativa
    if "idade" not in dados or not isinstance(dados["idade"], int) or dados["idade"] < 0:
        return jsonify({"erro": "O campo 'idade' deve ser um número inteiro positivo"}), 400

    #Valida se a matéria tem menos de 100 caracteres
    if "materia" not in dados or not isinstance(dados["materia"], str) or len(dados["materia"]) > 100 :
        return jsonify({"erro": "O campo 'materia' tem que ser string e no máximo 100 caracteres "}), 400

    #Verifica se observacoes é do tipo string
    if "observacoes" in dados and not isinstance(dados["observacoes"], str):
        return jsonify({"erro": "O campo 'observacoes' deve ser uma string"}), 400


    dici["professor"].append(dados)
    return jsonify(dados), 201

# atualizar um professor
def updateProfessor(idProfessor):
    professor = next((prof for prof in dici["professor"] if prof["id"] == idProfessor), None)

    if not professor:
        return jsonify({"erro": "Professor não encontrado"}), 404

    dados = request.json

    if "nome" in dados and not isinstance(dados["nome"], str)  or  dados["nome"].strip() == "" :
        return jsonify({"erro ": "Digite o nome corretamente"})
    if "idade" in dados:
        if not isinstance(dados["idade"], int) or dados["idade"] < 0:
            return jsonify({"erro": "O campo 'idade' deve ser um número inteiro positivo"}), 400

    if "materia" in dados:
        if not isinstance(dados["materia"], str):
            return jsonify({"erro": "O campo 'materia' deve ser uma string"}), 400
        if len(dados["materia"]) > 100:
            return jsonify({"erro": "O campo 'materia' deve ter no máximo 100 caracteres"}), 400

    if "observacoes" in dados:
        if not isinstance(dados["observacoes"], str):
            return jsonify({"erro": "O campo 'observacoes' deve ser uma string"}), 400

    professor["nome"] = dados["nome"]
    professor["idade"] = dados["idade"]
    professor["materia"] = dados["materia"]
    professor["observacoes"] = dados["observacoes"]
    return jsonify(professor), 201

# deletar um professor
def deleteProfessor(idProfessor):
    professores = dici["professor"]
    for professor in professores:
        if professor['id'] == idProfessor:
            dados = professor
            dici['professor'].remove(dados)
            dados=dici['professor'] 
            return jsonify(dados)

    return jsonify({"erro ": "Esse professor não existe"}), 404

