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
    return jsonify({"erro": "Aluno não encontrado"}), 404

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
    return jsonify(dados), 201

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
    for turma in turmas:
        if turma['id'] == idTurma:
            dados = turma
            return jsonify(dados)

@app.route('/turmas',methods=['POST'])
def createTurma():
    dados = request.json
    dici['turma'].append(dados)
    return jsonify(dados)

@app.route("/turmas/<int:idTurma>", methods=['PUT'])
def updateTurmas(idTurma):
    turmas = dici["turma"]
    for turma in turmas:
        if turma['id'] == idTurma:
            dados = request.json
            turma["id"] = dados['id']
            turma['descricao'] = dados['descricao']
            turma['ativo'] = dados['ativo']
            dados = request.json
            return jsonify(dados)


@app.route("/turmas/<int:idTurma>", methods=['DELETE'])        
def deleteTurmas(idTurma):
    turmas = dici["turma"]
    for turma in turmas:
        if turma['id'] == idTurma:
            dados = turma
            dici['turma'].remove(dados)
            dados=dici['turma'] 
            return jsonify(dados)


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
    return jsonify(alunos, professores)


import Erros

if __name__=="__main__":
    app.run(debug=True)

