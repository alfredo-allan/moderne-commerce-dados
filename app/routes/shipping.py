from flask import Blueprint, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

shipping_bp = Blueprint("shipping", __name__)  # Sem url_prefix


@shipping_bp.route("/shipping", methods=["POST"])
def calcular_frete():
    try:
        data = request.get_json()
        cep_destino = data.get("cep")
        produtos = data.get("produtos")

        if not cep_destino or not produtos:
            return jsonify({"error": "Dados incompletos"}), 400

        token = os.environ.get("MELHOR_ENVIO_TOKEN")
        email = os.environ.get("MELHOR_ENVIO_EMAIL")
        cep_origem = os.environ.get("MELHOR_ENVIO_CEP_ORIGEM")

        if not all([token, email, cep_origem]):
            return jsonify({"error": "Credenciais da API ausentes ou incompletas"}), 500

        url = "https://sandbox.melhorenvio.com.br/api/v2/me/shipment/calculate"  # Ajuste para endpoint correto

        payload = {
            "from": {"postal_code": cep_origem},
            "to": {"postal_code": cep_destino},
            "products": produtos,
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
            "User-Agent": email,  # Usar email conforme exigência da API
            "Accept": "application/json",
        }

        response = requests.post(url, headers=headers, json=payload)

        if not response.ok:
            return (
                jsonify(
                    {
                        "error": "Erro ao consultar frete",
                        "status_code": response.status_code,
                        "details": response.text,
                    }
                ),
                response.status_code,
            )

        return jsonify(response.json())

    except Exception as e:
        return jsonify({"error": "Erro interno no servidor", "details": str(e)}), 500


@shipping_bp.route("/shipping/cart", methods=["POST"])
def adicionar_ao_carrinho():
    try:
        data = request.get_json()
        token = os.environ.get("MELHOR_ENVIO_TOKEN")
        email = os.environ.get("MELHOR_ENVIO_EMAIL")

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
            "User-Agent": email,
            "Accept": "application/json",
        }

        url = "https://sandbox.melhorenvio.com.br/api/v2/me/cart"
        response = requests.post(
            url, headers=headers, json=[data]
        )  # Espera lista de objetos

        if not response.ok:
            return (
                jsonify(
                    {
                        "error": "Erro ao adicionar frete ao carrinho",
                        "details": response.text,
                    }
                ),
                response.status_code,
            )

        return jsonify(response.json()), 200
    except Exception as e:
        return jsonify({"error": "Erro interno", "details": str(e)}), 500


@shipping_bp.route("/shipping/checkout", methods=["POST"])
def pagar_etiqueta():
    try:
        data = request.get_json()  # Espera lista de IDs de etiquetas
        token = os.environ.get("MELHOR_ENVIO_TOKEN")
        email = os.environ.get("MELHOR_ENVIO_EMAIL")

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
            "User-Agent": email,
            "Accept": "application/json",
        }

        url = "https://sandbox.melhorenvio.com.br/api/v2/me/shipment/checkout"
        response = requests.post(url, headers=headers, json=data)

        if not response.ok:
            return (
                jsonify({"error": "Erro ao pagar etiqueta", "details": response.text}),
                response.status_code,
            )

        return jsonify(response.json()), 200
    except Exception as e:
        return jsonify({"error": "Erro interno", "details": str(e)}), 500


@shipping_bp.route("/shipping/generate", methods=["POST"])
def gerar_etiqueta():
    try:
        data = request.get_json()  # Espera lista de IDs
        token = os.environ.get("MELHOR_ENVIO_TOKEN")
        email = os.environ.get("MELHOR_ENVIO_EMAIL")

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
            "User-Agent": email,
            "Accept": "application/json",
        }

        url = "https://sandbox.melhorenvio.com.br/api/v2/me/shipment/generate"
        response = requests.post(url, headers=headers, json=data)

        if not response.ok:
            return (
                jsonify({"error": "Erro ao gerar etiqueta", "details": response.text}),
                response.status_code,
            )

        return jsonify(response.json()), 200
    except Exception as e:
        return jsonify({"error": "Erro interno", "details": str(e)}), 500
