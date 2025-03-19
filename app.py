#python -m venv *nome do ambiente*
#./*nome do ambiente*/Scripts/Activate
#pip install flask

from flask import Flask, jsonify, request # importando o Flask
from Erros import IdDuplicadoError, IdNegativoError, registrar_handlers

app = Flask(__name__)
registrar_handlers(app)  

dici = {
    "alunos":[
        {

            "id": 1,
            "nome": "MARCELOOOO",
            "idade": "40",
            "turma_id": "1",
            "data_de_nascimento": "10_10_2000",
            "nota_primeiro_semestre": "10",
            "nota_segundo_semestre": "8",
            "media_final": "9"

        },

        {

            "id": 2,
            "nome": "Marcos",
            "idade": "40",
            "turma_id": "1",
            "data_de_nascimento": "10_10_2000",
            "nota_primeiro_semestre": "10",
            "nota_segundo_semestre": "8",
            "media_final": "9"

        },

        {

            "id": 3,
            "nome": "Maria",
            "idade": "40",
            "turma_id": "1",
            "data_de_nascimento": "10_10_2000",
            "nota_primeiro_semestre": "10",
            "nota_segundo_semestre": "8",
            "media_final": "9"

        }       
    ],

    "professor":[
        {
            "id":1,
            "nome":"rafael",
            "idade": "",
            "materia": "",
            "observacoes": ""
        },
        {
            "id":2,
            "nome":"felipe",
            "idade": "",
            "materia": "",
            "observacoes": ""
        }
    ],

     "turma":[
        {
            "id":1,
            "descricao": "",
            "professor_id": "",
            "ativo": ""
        }
    ],
}


def validate_turma(data):
    if not isinstance(data.get('id'), int):
        return False, "ID deve ser um inteiro"
    if not isinstance(data.get('descricao'), str):
        return False, "Descrição deve ser uma string"
    if not isinstance(data.get('professor_id'), int):
        return False, "Professor ID deve ser um inteiro"
    if not isinstance(data.get('ativo'), str):
        return False, "Ativo deve ser uma string"
    return True, ""

#ALUNOS -------------------------------------------------------------------------------------        
#ALUNOS -------------------------------------------------------------------------------------        
#ALUNOS -------------------------------------------------------------------------------------        
# === Rota para pegar todos os alunos (GETTTT) ===
@app.route('/alunos', methods=['GET'])
def getAluno():
    return jsonify(dici['alunos'])

# === Rota para pegar um aluno por ID (GETTTTTTTT)  ===
@app.route("/alunos/<int:idAluno>", methods=['GET'])
def getAlunosId(idAluno):
    alunos = dici["alunos"]
    for aluno in alunos:
        if aluno["id"] == idAluno:
            return jsonify(aluno)
    return jsonify({"erro": "Aluno não encontrado"})

# === Rota para criar aluno (POSTTTTTTTTT)===
@app.route('/alunos', methods=['POST'])
def createAluno():
    dados = request.json
    alunos = dici['alunos']

    # Verifica se o ID já existe
    for aluno in alunos:
        if aluno['id'] == dados['id']:
            raise IdDuplicadoError("Já existe um aluno com esse ID")

    # Verifica se o ID é válido
    if dados.get('id') is None or dados['id'] < 1:
        raise IdNegativoError("O ID do aluno deve ser maior ou igual a 1")

    # Adiciona o aluno se passar nas verificações
    dici['alunos'].append(dados)
    return jsonify(dados)

@app.route('/alunos', methods=['POST'])

@app.route("/alunos/<int:idAluno>", methods=['PUT'])
def updateAlunos(idAluno):
    alunos = dici["alunos"]
    for aluno in alunos:
        if aluno["id"] == idAluno:
            dados = request.json

            aluno['nome'] = dados['nome']
            aluno["idade"] = dados["idade"]
            aluno["turma_id"] = dados["turma_id"]
            aluno["data_de_nascimento"] = dados["data_de_nascimento"]
            aluno["nota_primeiro_semestre"] =  dados["nota_primeiro_semestre"]
            aluno["nota_segundo_semestre"] = dados["nota_segundo_semestre"]
            aluno["media_final"] = dados["media_final"]
            return jsonify(aluno)


@app.route("/alunos/<int:idAluno>", methods=['DELETE'])
def deleteAlunos(idAluno):
    alunos = dici["alunos"]
    for aluno in alunos:
        if aluno['id'] == idAluno:
            dados = aluno
            dici['alunos'].remove(dados)
            dados=dici['alunos'] 
            return jsonify(dados)

        

#ALUNOS ---------------------------------------------------------------------------------------------
#PROFESSORES ---------
@app.route("/professores", methods=['GET'])
def getProfessor():
    dados = dici["professor"]
    return jsonify(dados)

@app.route("/professores/<int:idProfessor>", methods=['GET'])
def getProfessoresId(idProfessor):
    professores = dici["professor"]
    for professor in professores:
        if professor["id"] == idProfessor:
            dados = professor
            return jsonify(dados)

@app.route('/professores',methods=['POST'])
def createProfessor():
    dados = request.json
    dici['professor'].append(dados)
    return jsonify(dados)

@app.route("/professores/<int:idProfessor>", methods=['PUT'])
def updateProfessores(idProfessor):
    professores = dici["professor"]
    for professor in professores:
        if professor['id'] == idProfessor:
            dados = request.json
            professor['nome'] = dados['nome']
            professor['idade'] = dados['idade']
            professor['materia'] = dados['materia']
            professor['observacoes'] = dados['observacoes']
            dados = request.json
            return jsonify(dados)

@app.route("/professores/<int:idProfessor>", methods=['DELETE'])        
def deleteProfessores(idProfessor):
    professores = dici["professor"]
    for professor in professores:
        if professor['id'] == idProfessor:
            dados = professor
            dici["professor"].remove(dados)
            dados=dici['professor'] 
            return jsonify(dados)
        
#TURMAS --------
@app.route("/turmas", methods=['GET'])
def getTurma():
    dados = dici['turma']
    return jsonify(dados)

@app.route("/turmas/<int:idTurma>", methods=['GET'])
def getTurmasId(idTurma):
    turmas = dici["turma"]

    #verifica se o id passado existe em alguma turma
    #no proprio endpoint da erro se nao for int "<int:idTurma">
    for turma in turmas:
        if turma['id'] == idTurma:
            dados = turma
            return jsonify(dados)  
        else:
            return jsonify({"erro ": "Não existe essa turma"}), 404

@app.route('/turmas',methods=['POST'])
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
        return jsonify ({"erro ": "Ativo deve ser uma True ou False"}), 400
    
    dici['turma'].append(dados)
    return jsonify(dados)

@app.route("/turmas/<int:idTurma>", methods=['PUT'])
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


@app.route("/turmas/<int:idTurma>", methods=['DELETE'])        
def deleteTurmas(idTurma):
    turmas = dici["turma"]
    for turma in turmas:
        if turma['id'] == idTurma:
            dados = turma
            dici['turma'].remove(dados)
            dados=dici['turma'] 
            return jsonify(dados), 200
        
    return jsonify({"erro ": "Essa Turma não existe"}), 404


@app.route("/reseta", methods = ['POST', "DELETE"])
def resetaAlunosProfessroes():
    professores = []
    dici["professor"] = professores
    alunos = []
    dici["alunos"] = alunos
    for professor in professores:
        dici["professor"].remove(professor)
    for aluno in alunos:
        dici["aluno"].remove(aluno)
    return jsonify(alunos, professores), 200


import Erros

if __name__=="__main__":
    app.run(debug=True)

