from flask import request, jsonify
from .alunos_model import Aluno
from config import db
import datetime
from datetime import datetime
from turmas.turmas_model import Turma

def calcular_idade(data_nascimento):
    """Calcula a idade com base na data de nascimento."""
    data_nascimento = datetime.strptime(data_nascimento, "%d_%m_%Y")
    hoje = datetime.today()
    idade = hoje.year - data_nascimento.year - ((hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day))
    return idade

 
# === pegar todos os alunos ===
def getAluno():
    alunos = Aluno.query.all()
    return jsonify([aluno.to_dict() for aluno in alunos])

# === pegar um aluno por ID   ===
def getAlunosId(idAluno):
    aluno = Aluno.query.get(idAluno)
    if not aluno:
        return jsonify({'erro': 'Aluno não encontrada'}), 404  
    return jsonify(aluno.to_dict()), 200

# === criar aluno === #
def createAluno():
    dados = request.json

    # Verifica campos obrigatórios
    if "nome" not in dados or dados["nome"].strip() == "":
        return jsonify({"erro": "Preencha o nome"}), 400

    if "data_de_nascimento" not in dados:
        return jsonify({"erro": "Data de nascimento é obrigatória"}), 400

    if "turma_id" not in dados or not isinstance(dados["turma_id"], int):
        return jsonify({"erro": "O campo 'turma_id' é obrigatório e deve ser um inteiro"}), 400

    # Verifica se a turma existe
    turma = Turma.query.get(dados["turma_id"])
    if not turma:
        return jsonify({"erro": "Turma inexistente"}), 400

    # Validação e conversão da data de nascimento
    data_nascimento = dados["data_de_nascimento"]
    try:
        data_nascimento_obj = datetime.strptime(data_nascimento, "%d_%m_%Y").date()
    except ValueError:
        return jsonify({"erro": 'Formato inválido. Use "dd_mm_aaaa", como "10_10_2000"'}), 400

    # Validação das notas
    nota_primeiro = dados.get("nota_primeiro_semestre")
    nota_segundo = dados.get("nota_segundo_semestre")

    if nota_primeiro is not None:
        if not isinstance(nota_primeiro, (int, float)) or not (0 <= nota_primeiro <= 10):
            return jsonify({"erro": "Nota do primeiro semestre deve ser um número entre 0 e 10"}), 400

    if nota_segundo is not None:
        if not isinstance(nota_segundo, (int, float)) or not (0 <= nota_segundo <= 10):
            return jsonify({"erro": "Nota do segundo semestre deve ser um número entre 0 e 10"}), 400


    # Cria aluno
    novo_aluno = Aluno(
        nome=dados["nome"],
        turma_id=dados["turma_id"],
        data_de_nascimento=data_nascimento_obj,
        nota_primeiro_semestre=nota_primeiro,
        nota_segundo_semestre=nota_segundo
    )

    db.session.add(novo_aluno)
    db.session.commit()

    return jsonify({"mensagem": "Aluno criado com sucesso!", "aluno": novo_aluno.to_dict()}), 201

def updateAlunos(idAluno):
    aluno = Aluno.query.get(idAluno)
    if not aluno:
        return jsonify({"erro": "Aluno não encontrado"}), 404

    dados = request.json

    # Validação do nome
    if "nome" not in dados or dados["nome"].strip() == "":
        return jsonify({"erro": "Preencha o nome novamente"}), 400

    # Validação da data de nascimento
    if "data_de_nascimento" not in dados or dados["data_de_nascimento"].strip() == "":
        return jsonify({"erro": "Data de nascimento é obrigatória"}), 400
    try:
        data_nascimento_obj = datetime.strptime(dados["data_de_nascimento"], "%d_%m_%Y").date()
    except ValueError:
        return jsonify({"erro": 'Formato inválido. Use "DD_MM_YYYY", exemplo 10_10_2020'}), 400

    


    # Validação do turma_id
    if "turma_id" not in dados or dados["turma_id"] == "":
        return jsonify({"erro": "O campo 'turma_id' é obrigatório."}), 400
    if not isinstance(dados["turma_id"], int):
        return jsonify({"erro": "O campo 'turma_id' deve ser um número inteiro"}), 400
    from turmas.turmas_model import Turma
    turma = Turma.query.get(dados["turma_id"])
    if not turma:
        return jsonify({"erro": "Turma inexistente"}), 400

    # Validação das notas
    nota_primeiro = dados.get("nota_primeiro_semestre")
    nota_segundo = dados.get("nota_segundo_semestre")

    if nota_primeiro is not None:
        if not isinstance(nota_primeiro, (int, float)) or not (0 <= nota_primeiro <= 10):
            return jsonify({"erro": "Nota do primeiro semestre deve ser um número entre 0 e 10"}), 400

    if nota_segundo is not None:
        if not isinstance(nota_segundo, (int, float)) or not (0 <= nota_segundo <= 10):
            return jsonify({"erro": "Nota do segundo semestre deve ser um número entre 0 e 10"}), 400
    
    # Atualiza os dados do aluno
    aluno.nome = dados["nome"]
    aluno.data_de_nascimento = data_nascimento_obj
    aluno.turma_id = dados["turma_id"]
    if nota_primeiro is not None:
        aluno.nota_primeiro_semestre = nota_primeiro
    if nota_segundo is not None:
        aluno.nota_segundo_semestre = nota_segundo
    aluno.media_final = aluno.calcular_media_final(aluno.nota_primeiro_semestre, aluno.nota_segundo_semestre)


    db.session.commit()

    return jsonify({"mensagem": "Aluno atualizado com sucesso!", "aluno": aluno.to_dict()})
        
def deleteAlunos(idAluno):
    aluno = Aluno.query.get(idAluno)
    if not aluno:
        return jsonify({'erro': 'Aluno não encontrada'}), 404  
    db.session.delete(aluno)
    db.session.commit()
    return jsonify({'mensagem': 'Aluno apagado com sucesso!'}), 200
        

