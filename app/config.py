# app/config.py
import os
from dotenv import load_dotenv

load_dotenv()  # carrega o .env aqui ANTES de usar os.getenv


class Config:
    MP_ACCESS_TOKEN = os.getenv("MERCADO_PAGO_ACCESS_TOKEN")
    SQLALCHEMY_DATABASE_URI = "sqlite:///clientes.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
