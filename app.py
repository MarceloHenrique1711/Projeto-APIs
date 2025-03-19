#python -m venv *nome do ambiente*
#./*nome do ambiente*/Scripts/Activate
#pip install flask

from flask import Flask, jsonify, request # importando o Flask
from Erros import IdDuplicadoError, IdNegativoError, registrar_handlers
import datetime
from datetime import datetime

def calcular_idade(data_nascimento):
    """Calcula a idade com base na data de nascimento."""
    data_nascimento = datetime.strptime(data_nascimento, "%Y-%m-%d")
    hoje = datetime.today()
    idade = hoje.year - data_nascimento.year - ((hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day))
    return idade

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

# === Rota para criar aluno (POSTTTTTTTTT)=== #
@app.route('/alunos', methods=['POST'])
def createAluno():
    dados = request.json
    turmas = dici["turma"]

    # Verifica se o ID é um número inteiro
    if not isinstance(dados["id"], int):
        return jsonify({"erro": "O campo 'id' deve ser um número inteiro"}), 400
    
    # Verifica se o ID já esta sendo utilizado
    for aluno in dici['alunos']:
        if aluno['id'] == dados["id"]:
            return jsonify({"erro": "Esse ID ja foi utilizado"}),400

    #Verifica se o ID está vazio
    if "id" not in dados or dados["id"] == "":
        return jsonify({"erro": "Digite o ID novamente"}),400
    
    #Verifica se o iD nao é negativo
    if dados["id"] < 0:
        return jsonify({"erro": "ID não pode ser negativo"}),400

    #Verifica se o NOME está vazio
    if "nome" not in dados or dados["nome"] == "":
        return jsonify({"erro": "Preencha o nome"}),400
    
    #verifica se o DATA_DE_NASCIMENTO esta vazio
    if "data_de_nascimento" not in dados:
        return jsonify({"erro": "Data de nascimento é obrigatória"}),400
    
    data_nascimento = dados["data_de_nascimento"]
    
    # Verifica se a data está no formato dd_mm_yyyy
    if len(data_nascimento.split('_')) != 3:
        return jsonify({"erro": 'Data de nascimento deve conter apenas números, por exemplo "10_10_2024"'}),400
    
    dia, mes, ano = data_nascimento.split('_')
    # Verifica se dia, mês e ano são números
    if not dia.isdigit() or not mes.isdigit() or not ano.isdigit():
        return jsonify({"erro": 'Data de nascimento deve conter apenas números, por exemplo "10_10_2024"'}),400
    
    # Calcula a idade a partir da data de nascimento
    try:
        data_nascimento_obj = datetime.strptime(data_nascimento, "%d_%m_%Y")
        idade = (datetime.now() - data_nascimento_obj).days // 365  # Não calcula precisamente a idade dependendo da data que o usuario inseriu
    except ValueError:
        return jsonify({"erro": 'Data de nascimento deve conter apenas números, por exemplo "10_10_2024"'}),400
    
    turma_encontrado = False  # Variável para controlar se o professor foi encontrado

    for turma in turmas:
        if turma['id'] == dados["turma_id"]:
            turma_encontrado = True  # Marca como encontrado
            break  # Sai do loop assim que o professor for encontrado

    # Se turma não for encontrado, retorna um erro
    if not turma_encontrado:
        return jsonify({"error ": "Turma inexistente"}), 400
    
    
    # Valida a Nota do primeiro semestre de 1 a 10 porém não é obrigatorio que tenha  
    nota_primeiro_semestre = None
    if "nota_primeiro_semestre" in dados and dados["nota_primeiro_semestre"] != "" :
        try:
            nota_primeiro_semestre = float(dados["nota_primeiro_semestre"])
            if nota_primeiro_semestre < 0 or nota_primeiro_semestre > 10 or not isinstance (dados["nota_primeiro_semestre"], (float,int)):
                return jsonify({"erro": "Nota do primeiro semestre deve ser um numero entre 0 e 10"}), 400
        except ValueError:
            return jsonify({"erro": "Nota do primeiro semestre deve ser um número"}), 400
    
    # Valida a Nota do segundo semestre de 1 a 10 porém não é obrigatorio que tenha  
    nota_segundo_semestre = None
    if "nota_segundo_semestre" in dados and dados["nota_segundo_semestre"] != "":
        try:
            nota_segundo_semestre = float(dados["nota_segundo_semestre"])
            if nota_segundo_semestre < 0 or nota_segundo_semestre > 10 or not isinstance (dados["nota_segundo_semestre"], (float,int)):
                return jsonify({"erro": "Nota do segundo semestre deve ser um numero entre 0 e 10"}), 400
        except ValueError:
            return jsonify({"erro": "Nota do segundo semestre deve ser um número"}), 400
    
    #Se ambas as notas forem fornecidas calcula a media final
    media_final = None
    if nota_primeiro_semestre is not None and nota_segundo_semestre is not None:
        media_final = (nota_primeiro_semestre + nota_segundo_semestre) / 2
    
    # Adiciona os dados do aluno com a idade calculada
    # Adiciona a média final caso tenha
    dados["idade"] = idade
    if media_final is not None:
        dados["media_final"] = round(media_final, 2)  # Ele arredonda um número para cima ou para baixo dependendo da casa decimal 
    
    dici['alunos'].append(dados)
    
    return jsonify(dados),201


@app.route("/alunos/<int:idAluno>", methods=['PUT'])
def updateAlunos(idAluno):
    alunos = dici["alunos"]
    turmas = dici["turma"]
    
    # Verifica se o aluno existe
    aluno_encontrado = next((aluno for aluno in alunos if aluno["id"] == idAluno), None) 
    
    if aluno_encontrado is None:
        return jsonify({"erro": "Aluno não encontrado"}), 404  # Retorna erro 404 se não encontrar

    # Obtém os dados da requisição
    dados = request.json

    # Verifica se o NOME está vazio
    if "nome" not in dados or dados["nome"].strip() == "":
        return jsonify({"erro": "Preencha o nome novamente"}), 400

    # Verifica se o DATA_DE_NASCIMENTO não está vazio
    if "data_de_nascimento" not in dados or dados["data_de_nascimento"].strip() == "":
        return jsonify({"erro": "Data de nascimento é obrigatória"}), 400

    # Verifica se a data está no formato dd_mm_yyyy
    try:
        data_nascimento_obj = datetime.strptime(dados["data_de_nascimento"], "%d_%m_%Y")
        idade = (datetime.now() - data_nascimento_obj).days // 365
    except ValueError:
        return jsonify({"erro": 'Formato inválido. Use "DD_MM_YYYY", exemplo 10_10_2020'}), 400

    # Verifica se tem o TURMA_ID
    if "turma_id" not in dados or dados["turma_id"] == "":
        return jsonify({"erro": "O campo 'turma_id' é obrigatório."}), 400
    if not isinstance(dados["turma_id"], int):
        return jsonify({"erro": "O campo 'turma_id' deve ser um número inteiro"}), 400

    turma_encontrado = False  # Variável para controlar se o professor foi encontrado

    for turma in turmas:
        if turma['id'] == dados["turma_id"]:
            turma_encontrado = True  # Marca como encontrado
            break  # Sai do loop assim que o professor for encontrado

    # Se turma não for encontrado, retorna um erro
    if not turma_encontrado:
        return jsonify({"error ": "Turma inexistente"}), 400

    # Verifica se as notas são de 0 a 10
    nota_primeiro_semestre = None
    if "nota_primeiro_semestre" in dados and dados["nota_primeiro_semestre"] != "" :
        try:
            nota_primeiro_semestre = float(dados["nota_primeiro_semestre"])
            if nota_primeiro_semestre < 0 or nota_primeiro_semestre > 10 or not isinstance (dados["nota_primeiro_semestre"], (float,int)):
                return jsonify({"erro": "Nota do primeiro semestre deve ser um numero entre 0 e 10"}), 400
        except ValueError:
            return jsonify({"erro": "Nota do primeiro semestre deve ser um número"}), 400

    nota_segundo_semestre = None
    if "nota_segundo_semestre" in dados and dados["nota_segundo_semestre"] != "":
        try:
            nota_segundo_semestre = float(dados["nota_segundo_semestre"])
            if nota_segundo_semestre < 0 or nota_segundo_semestre > 10 or not isinstance (dados["nota_segundo_semestre"], (float,int)):
                return jsonify({"erro": "Nota do segundo semestre deve ser um numero entre 0 e 10"}), 400
        except ValueError:
            return jsonify({"erro": "Nota do segundo semestre deve ser um número"}), 400

    # Calcula a média final se ambas as notas forem fornecidas
    if nota_primeiro_semestre is not None and nota_segundo_semestre is not None:
        media_final = round((nota_primeiro_semestre + nota_segundo_semestre) / 2, 2)
    else:
        # Caso uma das notas não seja fornecida, mantém a média anterior ou ajusta conforme o dado disponível
        media_final = aluno_encontrado.get("media_final", None)

    # Atualiza os dados do aluno
    aluno_encontrado["nome"] = dados["nome"]
    aluno_encontrado["turma_id"] = dados["turma_id"]
    aluno_encontrado["data_de_nascimento"] = dados["data_de_nascimento"]
    aluno_encontrado["idade"] = idade

    # Atualiza notas e média final se foram fornecidas
    if nota_primeiro_semestre is not None:
        aluno_encontrado["nota_primeiro_semestre"] = nota_primeiro_semestre
    if nota_segundo_semestre is not None:
        aluno_encontrado["nota_segundo_semestre"] = nota_segundo_semestre
    if media_final is not None:
        aluno_encontrado["media_final"] = media_final

    return jsonify(aluno_encontrado)
        
@app.route("/alunos/<int:idAluno>", methods=['DELETE'])
def deleteAlunos(idAluno):
    alunos = dici["alunos"]
    for aluno in alunos:
        if aluno['id'] == idAluno:
            dados = aluno
            dici['alunos'].remove(dados)
            dados=dici['alunos'] 
            return jsonify(dados)
    return jsonify({"erro": "Esse Aluno não existe"})   
        

#ALUNOS ---------------------------------------------------------------------------------------------
#PROFESSORES ---------
# Rotas para professores
@app.route("/professores", methods=['GET'])
def getProfessores():
    return jsonify(dici["professor"])

#verifica se o id passado existe em alguma turma
#no proprio endpoint da erro se nao for int "<int:idTurma">
@app.route("/professores/<int:idProfessor>", methods=['GET'])
def getProfessorId(idProfessor):
    professores = dici["professor"]
    for professor in professores:
        if professor['id'] == idProfessor:
            dados = professor
            return jsonify(dados)
    return jsonify({"erro ": "Não existe esse professor"}), 404


# Rota para criar um professor
@app.route('/professores', methods=['POST'])
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

# Rota para atualizar um professor
@app.route("/professores/<int:idProfessor>", methods=['PUT'])
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
    return jsonify(professor)

# Rota para deletar um professor
@app.route("/professores/<int:idProfessor>", methods=['DELETE'])        
def deleteProfessor(idProfessor):
    professores = dici["professor"]
    for professor in professores:
        if professor['id'] == idProfessor:
            dados = professor
            dici['professor'].remove(dados)
            dados=dici['professor'] 
            return jsonify(dados), 200

    return jsonify({"erro ": "Esse professor não existe"}), 404

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
        return jsonify ({"erro ": "Ativo deve ser True ou False"}), 400
    
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

