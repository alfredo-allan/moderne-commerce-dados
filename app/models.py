from .extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy import Integer, String, Float, DateTime, Column, ForeignKey, JSON


class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo_pessoa = db.Column(db.String(10), nullable=False)
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


class ShippingCalculation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cep_destino = db.Column(db.String(9), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    prazo_entrega = db.Column(db.String(50))
    servico = db.Column(db.String(100))
    data_calculo = db.Column(db.DateTime, default=datetime.utcnow)
    usuario = db.Column(db.String(100))


class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("cliente.id"), nullable=False)
    order_id = db.Column(db.Integer, nullable=False)
    mercado_pago_id = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(50), nullable=True)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(100), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_approved = db.Column(db.DateTime, nullable=True)
    transaction_details = db.Column(db.JSON, nullable=True)

    cliente = db.relationship("Cliente", backref=db.backref("payments", lazy=True))

    def __repr__(self):
        return f"<Payment {self.id} - Order {self.order_id} - Status {self.status}>"


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("cliente.id"), nullable=False)
    order_id = db.Column(
        db.String(100), nullable=False, unique=True
    )  # ID interno (frontend)

    mercado_pago_order_id = db.Column(db.String(100), nullable=True)
    mercado_pago_payment_id = db.Column(db.String(100), nullable=True)
    payment_type = db.Column(db.String(50), nullable=True)
    payment_status = db.Column(db.String(50), nullable=True)
    payment_status_detail = db.Column(db.String(100), nullable=True)

    products = db.Column(db.JSON, nullable=False)
    shipping_cost = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)

    status = db.Column(
        db.String(20), default="pending"
    )  # pending, confirmed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    confirmed_at = db.Column(db.DateTime, nullable=True)

    customer = db.relationship("Cliente", backref="orders")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "order_id": self.order_id,
            "mercado_pago_order_id": self.mercado_pago_order_id,
            "mercado_pago_payment_id": self.mercado_pago_payment_id,
            "payment_type": self.payment_type,
            "payment_status": self.payment_status,
            "payment_status_detail": self.payment_status_detail,
            "products": self.products,
            "shipping_cost": self.shipping_cost,
            "total": self.total,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "confirmed_at": (
                self.confirmed_at.isoformat() if self.confirmed_at else None
            ),
        }
