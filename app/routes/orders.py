from flask import Blueprint, request, jsonify
from app.models import Order, db
from datetime import datetime

orders_bp = Blueprint("orders", __name__, url_prefix="/orders")


@orders_bp.route("/pending", methods=["GET"])
def list_pending_orders():
    orders = Order.query.filter_by(status="pending").all()
    return jsonify([o.to_dict() for o in orders])


@orders_bp.route("/<int:order_id>/confirm", methods=["PUT"])
def confirm_order(order_id):
    order = Order.query.get_or_404(order_id)
    if order.status != "pending":
        return jsonify({"error": "Order is not pending."}), 400

    order.status = "confirmed"
    order.confirmed_at = datetime.utcnow()
    db.session.commit()
    return jsonify({"success": True, "message": "Order confirmed."})


@orders_bp.route("/<int:order_id>/cancel", methods=["PUT"])
def cancel_order(order_id):
    order = Order.query.get_or_404(order_id)
    if order.status != "pending":
        return jsonify({"error": "Order is not pending."}), 400

    order.status = "cancelled"
    db.session.commit()
    return jsonify({"success": True, "message": "Order cancelled."})


@orders_bp.route("/", methods=["POST"])
def create_order():
    data = request.json

    order = Order(
        user_id=data["user_id"],
        order_id=data["order_id"],
        mercado_pago_order_id=data.get("mercado_pago_order_id"),
        mercado_pago_payment_id=(
            str(data.get("mercado_pago_payment_id"))
            if data.get("mercado_pago_payment_id")
            else None
        ),
        payment_type=data.get("payment_type"),
        payment_status=data.get("payment_status"),
        payment_status_detail=data.get("payment_status_detail"),
        products=data["products"],
        shipping_cost=data["frete"],
        total=data["total"],
        status="pending",
    )

    db.session.add(order)
    db.session.commit()
    return jsonify({"success": True, "message": "Order created.", "order_id": order.id})
