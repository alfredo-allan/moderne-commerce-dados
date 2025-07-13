from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from app.extensions import db
from app.models import Cliente, ShippingCalculation
from app.routes.clients import clients_bp
from app.routes.shipping import shipping_bp
from app.routes.payment import payment_bp
from .config import Config  # ou DevelopmentConfig
from dotenv import load_dotenv

load_dotenv()  # Carrega o .env

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///clientes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config.from_object(Config)  # aplica a config com o token

# ✅ Configuração do CORS com suporte a credenciais
CORS(
    app,
    supports_credentials=True,
    resources={
        r"/*": {
            "origins": ["http://localhost:5173"],
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
        }
    },
)

# Inicialização das extensões
db.init_app(app)
migrate = Migrate(app, db)

# Criação do banco (se necessário)
with app.app_context():
    db.create_all()

# Registro dos blueprints
app.register_blueprint(clients_bp)
app.register_blueprint(shipping_bp)
print("✅ Blueprint 'shipping_bp' registrado com CORS ativo")
app.register_blueprint(payment_bp)
