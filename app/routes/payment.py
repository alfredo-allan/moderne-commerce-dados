# app/routes/payment_routes.py
import logging
import mercadopago
from flask import Blueprint, request, jsonify
from app.models import Cliente, Payment, db
from flask import current_app

payment_bp = Blueprint("payment", __name__, url_prefix="/payment")


@payment_bp.route("/create", methods=["POST", "OPTIONS"])
def create_payment_preference():
    if request.method == "OPTIONS":
        return "", 200  # Resposta rápida para o preflight

    try:
        data = request.get_json()
        logging.debug(f"Dados recebidos do frontend: {data}")

        amount = data.get("amount") or 0  # valor dos produtos
        frete = data.get("frete") or 0  # valor do frete
        total = float(amount) + float(frete)

        order_id = data.get("order_id")
        user_id = data.get("user_id")
        produtos = data.get("produtos", [])

        if not order_id or not user_id:
            return jsonify({"message": "order_id e user_id são obrigatórios"}), 400

        user = Cliente.query.get(user_id)
        if not user:
            return jsonify({"message": f"Cliente com ID {user_id} não encontrado"}), 404

        # Mapeia produtos individuais para a lista do Mercado Pago
        items = []
        for produto in produtos:
            items.append(
                {
                    "title": produto.get("name", "Produto"),
                    "quantity": int(produto.get("quantity", 1)),
                    "unit_price": float(produto.get("unitary_value", 0)),
                }
            )

        # Adiciona frete como item separado
        if frete > 0:
            items.append({"title": "Frete", "quantity": 1, "unit_price": float(frete)})

        preference_data = {
            "items": items,
            "payer": {"email": user.email},
            "external_reference": str(order_id),
            "notification_url": f"{request.url_root}payment/webhook",
            "back_urls": {
                "success": f"{request.url_root}payment/success",
                "failure": f"{request.url_root}payment/failure",
                "pending": f"{request.url_root}payment/pending",
            },
            "auto_return": "approved",
        }

        sdk = mercadopago.SDK(current_app.config["MP_ACCESS_TOKEN"])
        preference_response = sdk.preference().create(preference_data)

        if preference_response and preference_response["status"] == 201:
            pref_id = preference_response["response"]["id"]
            init_point = preference_response["response"]["init_point"]

            novo_pagamento = Payment(
                user_id=user_id,
                order_id=order_id,
                amount=total,
                status="pending",
                mercado_pago_id=pref_id,
            )
            db.session.add(novo_pagamento)
            db.session.commit()

            return jsonify({"init_point": init_point}), 200

        msg = preference_response.get("response", {}).get(
            "message", "Erro ao criar preferência"
        )
        return jsonify({"message": msg}), 500

    except Exception as e:
        logging.exception("Erro ao criar preferência")
        return jsonify({"message": str(e)}), 500


@payment_bp.route("/webhook", methods=["POST"])
def webhook_payment():
    notification_id = request.args.get("id")
    if not notification_id:
        return jsonify({"message": "ID de notificação ausente"}), 400

    try:
        sdk = mercadopago.SDK(current_app.config["MP_ACCESS_TOKEN"])
        payment_info = sdk.payment().get(notification_id)

        if payment_info["status"] != 200:
            msg = payment_info.get("response", {}).get("message", "Erro desconhecido")
            return jsonify({"message": msg}), 500

        data = payment_info["response"]["payment"]
        status = data["status"]
        mp_id = data["id"]
        ext_ref = data["external_reference"]
        method = data.get("payment_method_id")
        approved = data.get("date_approved")
        details = data.get("transaction_details")

        pagamento = Payment.query.filter_by(order_id=ext_ref).first()
        if not pagamento:
            return (
                jsonify({"message": f"Pagamento não encontrado para pedido {ext_ref}"}),
                404,
            )

        pagamento.mercado_pago_id = mp_id
        pagamento.status = status
        pagamento.payment_method = method
        pagamento.date_approved = approved
        pagamento.transaction_details = details
        db.session.commit()

        return jsonify({"success": True}), 200

    except Exception as e:
        logging.exception("Erro no webhook")
        return jsonify({"message": str(e)}), 500
