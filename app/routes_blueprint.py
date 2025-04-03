from flask import Blueprint, request, jsonify
from app.models import Cliente, db
from app.models import Budget, db
from datetime import datetime

routes_blueprint = Blueprint("routes", __name__)


@routes_blueprint.route("/clientes", methods=["POST"])
def criar_cliente():
    data = request.get_json()
    novo_cliente = Cliente(
        cliente=data["cliente"],
        empresa=data["empresa"],
        endereco=data.get("endereco"),
        telefone=data.get("telefone"),
        email=data.get("email"),
        redesocial=data.get("redesocial"),
        informacoes=data.get("informacoes"),
    )
    db.session.add(novo_cliente)
    db.session.commit()
    return jsonify({"message": "Cliente criado com sucesso!"}), 201


@routes_blueprint.route("/clientes", methods=["GET"])
def listar_clientes():
    clientes = Cliente.query.all()
    lista_clientes = []
    for cliente in clientes:
        lista_clientes.append(
            {
                "id": cliente.id,
                "cliente": cliente.cliente,
                "empresa": cliente.empresa,
                "endereco": cliente.endereco,
                "telefone": cliente.telefone,
                "email": cliente.email,
                "redesocial": cliente.redesocial,
                "informacoes": cliente.informacoes,
            }
        )
    return jsonify(lista_clientes)


@routes_blueprint.route("/budgets", methods=["POST"])
def criar_budget():
    data = request.get_json()
    novo_budget = Budget(
        empresa=data["empresa"],
        cliente=data["cliente"],
        data=datetime.strptime(data["data"], "%Y-%m-%dT%H:%M:%S.%fZ").date(),
        validade=data.get("validade"),
        nome_projeto=data.get("nomeProjeto"),
        descricao=data.get("descricao"),
        orcados=data.get("orcados"),
        total=data.get("total"),
        prazo=data.get("prazo"),
        frete=data.get("frete"),
        observacao=data.get("observacao"),
        cnpj=data.get("cnpj"),
        pagamento=data.get("pagamento"),
    )
    db.session.add(novo_budget)
    db.session.commit()
    return jsonify({"message": "Budget criado com sucesso!"}), 201


@routes_blueprint.route("/budgets", methods=["GET"])
def listar_budgets():
    budgets = Budget.query.all()
    lista_budgets = []
    for budget in budgets:
        lista_budgets.append(
            {
                "id": budget.id,
                "empresa": budget.empresa,
                "cliente": budget.cliente,
                "data": budget.data.isoformat(),
                "validade": budget.validade,
                "nomeProjeto": budget.nome_projeto,
                "descricao": budget.descricao,
                "orcados": budget.orcados,
                "total": budget.total,
                "prazo": budget.prazo,
                "frete": budget.frete,
                "observacao": budget.observacao,
                "cnpj": budget.cnpj,
                "pagamento": budget.pagamento,
            }
        )
    return jsonify(lista_budgets)


@routes_blueprint.route("/clientes/<int:id>", methods=["PUT"])
def atualizar_cliente(id):
    cliente = Cliente.query.get(id)
    if not cliente:
        return jsonify({"message": "Cliente não encontrado"}), 404

    data = request.get_json()
    cliente.cliente = data.get("cliente", cliente.cliente)
    cliente.empresa = data.get("empresa", cliente.empresa)
    cliente.endereco = data.get("endereco", cliente.endereco)
    cliente.telefone = data.get("telefone", cliente.telefone)
    cliente.email = data.get("email", cliente.email)
    cliente.redesocial = data.get("redesocial", cliente.redesocial)
    cliente.informacoes = data.get("informacoes", cliente.informacoes)

    db.session.commit()
    return jsonify({"message": "Cliente atualizado com sucesso!"}), 200


@routes_blueprint.route("/clientes/<int:id>", methods=["DELETE"])
def deletar_cliente(id):
    cliente = Cliente.query.get(id)
    if not cliente:
        return jsonify({"message": "Cliente não encontrado"}), 404

    db.session.delete(cliente)
    db.session.commit()
    return jsonify({"message": "Cliente deletado com sucesso!"}), 200


@routes_blueprint.route("/budgets/<int:id>", methods=["PUT"])
def atualizar_budget(id):
    budget = Budget.query.get(id)
    if not budget:
        return jsonify({"message": "Budget não encontrado"}), 404

    data = request.get_json()
    budget.empresa = data.get("empresa", budget.empresa)
    budget.cliente = data.get("cliente", budget.cliente)
    budget.data = datetime.strptime(
        data.get("data"), "%Y-%m-%dT%H:%M:%S.%fZ"
    ).date()  # keep this line.

    budget.validade = data.get("validade", budget.validade)
    budget.nome_projeto = data.get("nomeProjeto", budget.nome_projeto)
    budget.descricao = data.get("descricao", budget.descricao)
    budget.orcados = data.get("orcados", budget.orcados)
    budget.total = data.get("total", budget.total)
    budget.prazo = data.get("prazo", budget.prazo)
    budget.frete = data.get("frete", budget.frete)
    budget.observacao = data.get("observacao", budget.observacao)
    budget.cnpj = data.get("cnpj", budget.cnpj)
    budget.pagamento = data.get("pagamento", budget.pagamento)

    db.session.commit()
    return jsonify({"message": "Budget atualizado com sucesso!"}), 200


@routes_blueprint.route("/budgets/<int:id>", methods=["DELETE"])
def deletar_budget(id):
    budget = Budget.query.get(id)
    if not budget:
        return jsonify({"message": "Budget não encontrado"}), 404

    db.session.delete(budget)
    db.session.commit()
    return jsonify({"message": "Budget deletado com sucesso!"}), 200


@routes_blueprint.route("/budgets/<int:id>", methods=["GET"])
def buscar_budget(id):
    budget = Budget.query.get(id)
    if not budget:
        return jsonify({"message": "Budget não encontrado"}), 404

    budget_data = {
        "id": budget.id,
        "empresa": budget.empresa,
        "cliente": budget.cliente,
        "data": budget.data.isoformat(),
        "validade": budget.validade,
        "nomeProjeto": budget.nome_projeto,
        "descricao": budget.descricao,
        "orcados": budget.orcados,
        "total": budget.total,
        "prazo": budget.prazo,
        "frete": budget.frete,
        "observacao": budget.observacao,
        "cnpj": budget.cnpj,
        "pagamento": budget.pagamento,
    }
    return jsonify(budget_data), 200
