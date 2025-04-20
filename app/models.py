# app/models.py
from .extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo_pessoa = db.Column(db.String(10), nullable=False)  # 'fisica' ou 'juridica'
    nome = db.Column(db.String(120), nullable=False)
    telefone = db.Column(db.String(20))
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(128), nullable=False)
    cpf = db.Column(db.String(14), unique=True)
    cnpj = db.Column(db.String(18), unique=True)
    razao_social = db.Column(db.String(120))
    cep = db.Column(db.String(9))
    rua = db.Column(db.String(100))
    numero = db.Column(db.String(10))
    bairro = db.Column(db.String(60))
    cidade = db.Column(db.String(60))

    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def check_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

    def __repr__(self):
        return f"<Cliente {self.nome} ({self.tipo_pessoa})>"