#python -m venv *nome do ambiente*
#./*nome do ambiente*/Scripts/Activate
#pip install flask

from flask import Flask, jsonify, request # importando o Flask

dici = {
    "alunos":[
        
            
        
    ],

    "professor":[
        {
            "id":1,
            "nome":"rafael",
            "idade": "",
            "materia": "",
            "observações": ""
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


app = Flask(__name__) # criando um novo objeto a partir do molde - métodos e propriedads

@app.route("/alunos", methods = ['GET']) #Criando minha rota
def getAluno(): # função do endpoint "/alunos" com verbo "GET"
    dados=dici['alunos'] # da chave "alunos" me retorna uma lista
    return jsonify(dados) # dicionario to json

@app.route('/alunos',methods=['POST'])
def createAluno():
    dados = request.json
    dici['alunos'].append(dados)
    return jsonify(dados)

@app.route("/alunos/<int:idAluno>", methods=['PUT'])
def updateAlunos(idAluno):
    alunos = dici["alunos"]
    for aluno in alunos:
        if aluno['id'] == idAluno:
            dados = request.json

            aluno['nome'] = dados['nome']
            aluno["idade"] = dados["idade"]
            aluno["turma_id"] = dados["turma_id"]
            aluno["data_de_nascimento"] = dados["data_de_nascimento"]
            aluno["nota_primeiro_semestre"] =  dados["nota_primeiro_semestre"]
            aluno["nota_segundo_semestre"] = dados["nota_segundo_semestre"]
            aluno["media_final"] = dados["media_final"]
            return jsonify(dados)
        else:
            return jsonify("aluno nao encontrado")

@app.route("/alunos/<int:idAluno>", methods=['DELETE'])
def deleteAlunos(idAluno):
    alunos = dici["alunos"]
    for aluno in alunos:
        if aluno['id'] == idAluno:
            dados = request.json
            dici['alunos'].remove(dados)
            dados=dici['alunos'] 
            return jsonify(dados)
        else:
            return jsonify("aluno nao encontrado")

if __name__=="__main__":
    app.run(debug=True)
