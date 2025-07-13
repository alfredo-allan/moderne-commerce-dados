from flask import Blueprint, request, jsonify
from app.models import Cliente, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash

clients_bp = Blueprint("clients", __name__, url_prefix="/clients")


@clients_bp.route("", methods=["POST"])
def register_client():
    data = request.get_json()
    tipo_pessoa = "fisica" if data.get("cpf") else "juridica"

    # Validações básicas
    if tipo_pessoa == "fisica" and not data.get("cpf"):
        return jsonify({"error": "CPF é obrigatório para pessoa física"}), 400
    if tipo_pessoa == "juridica" and not data.get("cnpj"):
        return jsonify({"error": "CNPJ é obrigatório para pessoa jurídica"}), 400
    if tipo_pessoa == "juridica" and not data.get("razao_social"):
        return (
            jsonify({"error": "Razão Social é obrigatória para pessoa jurídica"}),
            400,
        )
    if not all(k in data for k in ("nome", "email", "senha", "endereco")):
        return jsonify({"error": "Campos obrigatórios ausentes"}), 400
    if not all(
        k in data["endereco"] for k in ("cep", "rua", "numero", "bairro", "cidade")
    ):
        return jsonify({"error": "Campos de endereço obrigatórios ausentes"}), 400

    # Verificações explícitas antes do commit
    email = data["email"].strip().lower()
    if Cliente.query.filter_by(email=email).first():
        return jsonify({"error": "E-mail já está em uso"}), 409

    if data.get("cpf"):
        cpf = data["cpf"].strip().replace(".", "").replace("-", "")
        if Cliente.query.filter_by(cpf=cpf).first():
            return jsonify({"error": "CPF já está em uso"}), 409
    else:
        cpf = None

    if data.get("cnpj"):
        cnpj = data["cnpj"].strip().replace(".", "").replace("/", "").replace("-", "")
        if Cliente.query.filter_by(cnpj=cnpj).first():
            return jsonify({"error": "CNPJ já está em uso"}), 409
    else:
        cnpj = None

    novo_cliente = Cliente(
        tipo_pessoa=tipo_pessoa,
        nome=data["nome"].strip(),
        telefone=data.get("telefone"),
        email=email,
        cpf=cpf,
        cnpj=cnpj,
        razao_social=data.get("razao_social"),
        cep=data["endereco"]["cep"],
        rua=data["endereco"]["rua"],
        numero=data["endereco"]["numero"],
        bairro=data["endereco"]["bairro"],
        cidade=data["endereco"]["cidade"],
    )
    novo_cliente.set_senha(data["senha"])

    try:
        db.session.add(novo_cliente)
        db.session.commit()
        return (
            jsonify(
                {"message": "Cliente registrado com sucesso!", "id": novo_cliente.id}
            ),
            201,
        )
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": f"Erro de integridade: {str(e)}"}), 409

    data = request.get_json()
    tipo_pessoa = "fisica" if data.get("cpf") else "juridica"

    if tipo_pessoa == "fisica" and not data.get("cpf"):
        return jsonify({"error": "CPF é obrigatório para pessoa física"}), 400
    if tipo_pessoa == "juridica" and not data.get("cnpj"):
        return jsonify({"error": "CNPJ é obrigatório para pessoa jurídica"}), 400
    if tipo_pessoa == "juridica" and not data.get("razao_social"):
        return (
            jsonify({"error": "Razão Social é obrigatória para pessoa jurídica"}),
            400,
        )
    if not all(k in data for k in ("nome", "email", "senha", "endereco")):
        return jsonify({"error": "Campos obrigatórios ausentes"}), 400
    if not all(
        k in data["endereco"] for k in ("cep", "rua", "numero", "bairro", "cidade")
    ):
        return jsonify({"error": "Campos de endereço obrigatórios ausentes"}), 400

    novo_cliente = Cliente(
        tipo_pessoa=tipo_pessoa,
        nome=data["nome"],
        telefone=data.get("telefone"),
        email=data["email"],
        cpf=data.get("cpf"),
        cnpj=data.get("cnpj"),
        razao_social=data.get("razao_social"),
        cep=data["endereco"]["cep"],
        rua=data["endereco"]["rua"],
        numero=data["endereco"]["numero"],
        bairro=data["endereco"]["bairro"],
        cidade=data["endereco"]["cidade"],
    )
    novo_cliente.set_senha(data["senha"])

    try:
        db.session.add(novo_cliente)
        db.session.commit()
        return (
            jsonify(
                {"message": "Cliente registrado com sucesso!", "id": novo_cliente.id}
            ),
            201,
        )
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Email ou CPF/CNPJ já cadastrado"}), 409


@clients_bp.route("/login", methods=["POST"])
def login_client():
    data = request.get_json()
    email = data.get("email")
    senha = data.get("senha")

    if not email or not senha:
        return jsonify({"error": "Email e senha são obrigatórios"}), 400

    cliente = Cliente.query.filter_by(email=email).first()

    if cliente and cliente.check_senha(senha):
        return (
            jsonify(
                {
                    "id": cliente.id,
                    "nome": cliente.nome,
                    "email": cliente.email,
                    "tipoPessoa": cliente.tipo_pessoa,
                }
            ),
            200,
        )
    else:
        return jsonify({"error": "Credenciais inválidas"}), 401


@clients_bp.route("/<int:client_id>", methods=["GET"])
def get_client(client_id):
    cliente = Cliente.query.get_or_404(client_id)
    return (
        jsonify(
            {
                "id": cliente.id,
                "tipo_pessoa": cliente.tipo_pessoa,
                "nome": cliente.nome,
                "telefone": cliente.telefone,
                "email": cliente.email,
                "cpf": cliente.cpf,
                "cnpj": cliente.cnpj,
                "razao_social": cliente.razao_social,
                "endereco": {
                    "cep": cliente.cep,
                    "rua": cliente.rua,
                    "numero": cliente.numero,
                    "bairro": cliente.bairro,
                    "cidade": cliente.cidade,  # <- aqui estava o erro
                },
            }
        ),
        200,
    )


@clients_bp.route("/<int:client_id>", methods=["PUT"])
def update_client(client_id):
    cliente = Cliente.query.get_or_404(client_id)
    data = request.get_json()

    cliente.nome = data.get("nome", cliente.nome)
    cliente.telefone = data.get("telefone", cliente.telefone)
    cliente.email = data.get("email", cliente.email)
    if data.get("senha"):
        cliente.set_senha(data["senha"])
    cliente.cep = data.get("endereco", {}).get("cep", cliente.cep)
    cliente.rua = data.get("endereco", {}).get("rua", cliente.rua)
    cliente.numero = data.get("endereco", {}).get("numero", cliente.numero)
    cliente.bairro = data.get("endereco", {}).get("bairro", cliente.bairro)
    cliente.cidade = data.get("endereco", {}).get("cidade", cliente.cidade)

    try:
        db.session.commit()
        return jsonify({"message": "Cliente atualizado com sucesso!"}), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Email já cadastrado"}), 409


@clients_bp.route("/<int:client_id>", methods=["DELETE"])
def delete_client(client_id):
    cliente = Cliente.query.get_or_404(client_id)
    db.session.delete(cliente)
    db.session.commit()
    return jsonify({"message": "Cliente deletado com sucesso!"}), 200


# Nova rota para obter todos os clientes
@clients_bp.route("/secret_list_client", methods=["GET"])
def get_all_clients():
    clientes = Cliente.query.all()  # Busca todos os clientes no banco de dados
    lista_de_clientes = []
    for cliente in clientes:
        # Cria uma lista de dicionários, onde cada dicionário representa um cliente
        lista_de_clientes.append(
            {
                "id": cliente.id,
                "tipo_pessoa": cliente.tipo_pessoa,
                "nome": cliente.nome,
                "telefone": cliente.telefone,
                "email": cliente.email,
                "cpf": cliente.cpf,
                "cnpj": cliente.cnpj,
                "razao_social": cliente.razao_social,
                "endereco": {
                    "cep": cliente.cep,
                    "rua": cliente.rua,
                    "numero": cliente.numero,
                    "bairro": cliente.bairro,
                    "cidade": cliente.cidade,
                },
            }
        )
    return jsonify(lista_de_clientes), 200  # Retorna a lista como JSON
