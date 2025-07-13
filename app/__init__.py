# app/__init__.py
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from app.extensions import db
from app.routes.clients import clients_bp
from app.routes.shipping import shipping_bp
from app.routes.payment import payment_bp
from app.config import Config

app = Flask(__name__)
app.config.from_object(Config)
