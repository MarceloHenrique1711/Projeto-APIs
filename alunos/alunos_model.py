from datetime import datetime
from config import db

class Aluno(db.Model):
    __tablename__ = "alunos"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    idade = db.Column(db.Integer, nullable=False)  # Este campo pode ser preenchido pelo cálculo no momento da criação
    turma_id = db.Column(db.Integer, db.ForeignKey('turmas.id'), nullable=False)
    data_de_nascimento = db.Column(db.Date, nullable=False)
    nota_primeiro_semestre = db.Column(db.Float, nullable=False)
    nota_segundo_semestre = db.Column(db.Float, nullable=False)
    media_final = db.Column(db.Float, nullable=False)  # Calculado como a média das notas

    turma = db.relationship('Turma', backref='alunos')

    def __init__(self, nome, turma_id, data_de_nascimento, nota_primeiro_semestre, nota_segundo_semestre):
        self.nome = nome
        self.turma_id = turma_id
        self.data_de_nascimento = data_de_nascimento
        self.nota_primeiro_semestre = nota_primeiro_semestre
        self.nota_segundo_semestre = nota_segundo_semestre
        # Calculando a idade diretamente ao criar o aluno
        self.idade = self.calcular_idade(data_de_nascimento)
        # Calculando a média final diretamente ao criar o aluno
        self.media_final = self.calcular_media_final(nota_primeiro_semestre, nota_segundo_semestre)

    def calcular_idade(self, data_nascimento):
        """Calcula a idade com base na data de nascimento."""
        hoje = datetime.today()
        # Calculando a idade considerando mês e dia
        idade = hoje.year - data_nascimento.year - ((hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day))
        return idade

    def calcular_media_final(self, nota_primeiro_semestre, nota_segundo_semestre):
        """Calcula a média final do aluno."""
        if nota_primeiro_semestre is not None and nota_segundo_semestre is not None:
            return (nota_primeiro_semestre + nota_segundo_semestre) / 2
        return 0

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'idade': self.idade,
            'turma_id': self.turma_id,
            'data_de_nascimento': self.data_de_nascimento.strftime("%d_%m_%Y"),
            'nota_primeiro_semestre': self.nota_primeiro_semestre,
            'nota_segundo_semestre': self.nota_segundo_semestre,
            'media_final': self.media_final
        }
