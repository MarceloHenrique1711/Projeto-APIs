from flask import jsonify, request #pip install flask
from dicionario import *
from config import db

class Turma(db.Model):
    __tablename__ = "turmas"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descricao = db.Column(db.String(100), nullable=False)
    professor_id = db.Column(db.Integer, db.ForeignKey('professores.id'), nullable=False)  # Chave estrangeira
    ativo = db.Column(db.Boolean, default=True)

    # Relacionamento com o professor
    professor = db.relationship('Professor', backref='turmas')

    def __init__(self, descricao, professor_id, ativo):
        self.descricao = descricao
        self.professor_id = professor_id
        self.ativo = ativo

    def to_dict(self):
        return {
            'turma_id': self.id,
            'descricao': self.descricao,
            'ativo': self.ativo,
            'professor_id': self.professor_id,
        }
