from app.extensions import db


class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente = db.Column(db.String(100), nullable=False)
    empresa = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(200))
    telefone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    redesocial = db.Column(db.String(100))
    informacoes = db.Column(db.Text)

    def __repr__(self):
        return f"<Cliente {self.cliente}>"


class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    empresa = db.Column(db.String(255), nullable=False)
    cliente = db.Column(db.String(255), nullable=False)
    data = db.Column(db.Date, nullable=False)
    validade = db.Column(db.String(255))
    nome_projeto = db.Column(db.String(255))
    descricao = db.Column(db.Text)
    orcados = db.Column(db.Text)
    total = db.Column(db.Text)
    prazo = db.Column(db.String(255))
    frete = db.Column(db.Text)
    observacao = db.Column(db.Text)
    cnpj = db.Column(db.String(255))
    pagamento = db.Column(db.Text)

    def __repr__(self):
        return f"<Budget {self.nome_projeto}>"  # Correção aqui
