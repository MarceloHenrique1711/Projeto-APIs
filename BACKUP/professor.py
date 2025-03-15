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


app = Flask(__name__) # criando um novo objeto a partir do molde - métodos e propriedads


@app.route("/professores", methods=['GET'])
def getProfessor():
    dados = dici['professores']
    return jsonify(dados)

@app.route('/professores',methods=['POST'])
def createProfessor():
    dados = request.json
    dici['professores'].append(dados)
    return jsonify(dados)

@app.route("/professores/<int:idProfessor>", methods=['PUT'])
def updateProfessores(idProfessor):
    professores = dici["professores"]
    for professor in professores:
        if professor['id'] == idProfessor:
            dados = request.json
            professor['nome'] = dados['nome']
            professor['idade'] = dados['idade']
            professor['materia'] = dados['materia']
            professor['observacoes'] = dados['observacoes']
            dados = request.json
            return jsonify(dados)
        else:
            return jsonify("professor nao encontrado")

@app.route("/professores/<int:idProfessor>", methods=['DELETE'])        
def deleteProfessores(idProfessor):
    professores = dici["professores"]
    for professor in professores:
        if professor['id'] == idProfessor:
            dados = request.json
            dici['professor'].remove(dados)
            dados=dici['professor'] 
            return jsonify(dados)
        else:
            return jsonify("professor nao encontrado")


if __name__=="__main__":
    app.run(debug=True)