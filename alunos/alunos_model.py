import datetime
from datetime import datetime
from flask import jsonify, request
from dicionario import *

def calcular_idade(data_nascimento):
    """Calcula a idade com base na data de nascimento."""
    data_nascimento = datetime.strptime(data_nascimento, "%Y-%m-%d")
    hoje = datetime.today()
    idade = hoje.year - data_nascimento.year - ((hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day))
    return idade

 
# === pegar todos os alunos ===
def getAluno():
    return jsonify(dici['alunos'])

# === pegar um aluno por ID   ===
def getAlunosId(idAluno):
    alunos = dici["alunos"]
    for aluno in alunos:
        if aluno["id"] == idAluno:
            return jsonify(aluno)
    return jsonify({"erro": "Aluno não encontrado"}), 404

# === criar aluno === #
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
    
    # Antes de qualquer verificação com o campo 'turma_id', verifique sua existência
    if "turma_id" not in dados or str(dados["turma_id"]).strip() == "":
        return jsonify({"erro": "O campo 'turma_id' é obrigatório."}), 400
    
    turma_encontrado = False  # Variável para controlar se o turma foi encontrado

    for turma in turmas:
        if turma['id'] == dados["turma_id"]:
            turma_encontrado = True  # Marca como encontrado
            break  # Sai do loop assim que o turma for encontrado

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
        
def deleteAlunos(idAluno):
    alunos = dici["alunos"]
    for aluno in alunos:
        if aluno['id'] == idAluno:
            dados = aluno
            dici['alunos'].remove(dados)
            dados=dici['alunos'] 
            return jsonify(dados)
    return jsonify({"erro": "Esse Aluno não existe"}), 404 
        

