#python -m venv *nome do ambiente*
#./*nome do ambiente*/Scripts/Activate
#pip install flask

from flask import Flask, jsonify, request # importando o Flask

dici = {
    "alunos":[
        {
            "id":1,
            "nome":"caio",
            "idade": "10",
            "turma_id": "1",
            "data_de_nascimento": "",
            "nota_primeiro_semestre": "",
            "nota_segundo_semestre": "",
            "media_final": ""
        }
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


@app.route("/turmas", methods=['GET'])
def getTurma():
    dados = dici['turmas']
    return jsonify(dados)

@app.route('/turmas',methods=['POST'])
def createTurma():
    dados = request.json
    dici['turmas'].append(dados)
    return jsonify(dados)

@app.route("/turmas/<int:idTurma>", methods=['PUT'])
def updateTurmas(idTurma):
    turmas = dici["turmas"]
    for turma in turmas:
        if turma['id'] == idTurma:
            dados = request.json
            turma["id"] = dados['id']
            turma['descricao'] = dados['descricao']
            turma['ativo'] = dados['ativo']
            dados = request.json
            return jsonify(dados)
        else:
            return jsonify("turma nao encontrada")

@app.route("/turmas/<int:idTurma>", methods=['DELETE'])        
def deleteTurmas(idTurma):
    turmas = dici["professores"]
    for turma in turmas:
        if turma['id'] == idTurma:
            dados = request.json
            dici['turma'].remove(dados)
            dados=dici['turma'] 
            return jsonify(dados)
        else:
            return jsonify("professor nao encontrado")


if __name__=="__main__":
    app.run(debug=True)