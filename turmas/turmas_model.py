from flask import jsonify, request
from dicionario import *


#TURMAS --------
def getTurma():
    dados = dici['turma']
    return jsonify(dados)

def getTurmasId(idTurma):
    turmas = dici["turma"]

    #verifica se o id passado existe em alguma turma
    #no proprio endpoint da erro se nao for int "<int:idTurma">
    for turma in turmas:
        if turma['id'] == idTurma:
            dados = turma
            return jsonify(dados)  

    return jsonify({"erro ": "Não existe essa turma"}), 404

def createTurma():
    dados = request.json
    professores = dici["professor"]
    turmas = dici["turma"]

    #verifica se o id ja é usado em outra turma
    for turma in turmas:
        if turma['id'] == dados['id']:
            return jsonify({"erro ": "ID da turma repetido"}), 400

    #verifica se o id é inteiro
    if not isinstance(dados.get('id'), int):
        return jsonify({"error ": "ID deve ser um inteiro"}), 400
    
    #verifica se o id é positivo
    if dados.get("id") < 1:
        return jsonify({"error ": "ID deve ser positivo"}), 400

    #verifica se descricao é string
    if not isinstance(dados.get('descricao'), str):
        return jsonify ({"erro ": "Descricao deve ser uma string"}), 400
    
    #verifica se decricao tem no max 100 caractere
    if not len(dados.get('descricao')) <= 100:
        return jsonify ({"erro: ": "Descricao deve ter no máximo 100 caracteres"}), 400
    
    professor_encontrado = False  # Variável para controlar se o professor foi encontrado

    for professor in professores:
        if professor['id'] == dados["professor_id"]:
            professor_encontrado = True  # Marca como encontrado
            break  # Sai do loop assim que o professor for encontrado

    # Se o professor não for encontrado, retorna um erro
    if not professor_encontrado:
        return jsonify({"error ": "Professor inexistente"}), 400

    #verifica se ativo é true ou false
    if not isinstance(dados.get('ativo'), bool):
        return jsonify ({"erro ": "Ativo deve ser True ou False"}), 400
    
    dici['turma'].append(dados)
    return jsonify(dados)

def updateTurmas(idTurma):
    turmas = dici["turma"]
    professores = dici["professor"]
    for turma in turmas:
        if turma['id'] == idTurma:
            dados = request.json

            #verifica se o id ja é usado em outra turma
            for turma in turmas:
                if turma['id'] == dados['id']:
                    return jsonify({"erro ": "ID da turma repetido"}), 400

            #verifica se o id é inteiro
            if not isinstance(dados.get('id'), int):
                return jsonify({"error ": "ID deve ser um inteiro"}), 400
            
            #verifica se o id é positivo
            if dados.get("id") < 1:
                return jsonify({"error ": "ID deve ser positivo"}), 400

            #verifica se descricao é string
            if not isinstance(dados.get('descricao'), str):
                return jsonify ({"erro ": "Descricao deve ser uma string"}), 400
            
            #verifica se decricao tem no max 100 caractere
            if not len(dados.get('descricao')) <= 100:
                return jsonify ({"erro : ": "Descricao deve ter no máximo 100 caracteres"}), 400



            # Verifica se o professor existe para ser atribuído à turma
            if not isinstance(dados.get('professor_id'), int) or dados.get('professor_id') < 1:
                return jsonify({"error": "Professor ID deve ser um número inteiro positivo"}), 400

            # Verifica se o professor existe
            professor_encontrado = False
            
            for professor in professores:
                if professor['id'] == dados['professor_id']:
                    professor_encontrado = True
                    break
                
            if not professor_encontrado:  
                return jsonify({"error": "Professor inexistente"}), 400
           
            #verifica se ativo é true ou false
            if not isinstance(dados.get('ativo'), bool):
                return jsonify ({"erro ": "Ativo deve ser uma True ou False"}), 400
            
            turma["id"] = dados['id']
            turma['descricao'] = dados['descricao']
            turma['professor_id'] = dados['professor_id']
            turma['ativo'] = dados['ativo']
            return jsonify(dados), 200
    return jsonify({"erro ": "Turma não encontrada"}), 404
   
def deleteTurmas(idTurma):
    turmas = dici["turma"]
    for turma in turmas:
        if turma['id'] == idTurma:
            dados = turma
            dici['turma'].remove(dados)
            dados=dici['turma'] 
            return jsonify(dados), 200
        
    return jsonify({"erro ": "Essa Turma não existe"}), 404

def resetaAlunosProfessores():
    try:
        dici["professor"] = []
        dici["alunos"] = []
        return jsonify({
            "alunos": dici["alunos"],
            "professores": dici["professor"]
        }), 200
    except Exception as e:
        return jsonify({"erro": f"Erro ao tentar resetar os dados: {str(e)}"}), 404
