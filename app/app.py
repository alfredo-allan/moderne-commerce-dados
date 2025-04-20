from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from app.extensions import db
from app.models import Cliente
from app.routes.clients import clients_bp  # <- CORRETO AQUI

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///clientes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

CORS(
    app,
    resources={
        r"/*": {
            "origins": ["http://localhost:3000", "http://127.0.0.1:3000"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "headers": ["Content-Type", "Authorization"],
            "supports_credentials": True,
        }
    },
)

db.init_app(app)
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()

# REGISTRA COM O NOME CORRETO
app.register_blueprint(clients_bp)
