"""
Flask API for wine production, processing, commercialization, import and export data.

This API provides authenticated access to Brazilian wine industry data from Embrapa.
"""
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flasgger import Swagger
from libs.users import users
from libs.request_function import my_request
from errors import InvalidParam, CustomConnectionError


app = Flask(__name__)

# Configuração básica do JWT
app.config['JWT_SECRET_KEY'] = 'mykey'  # Troque para algo mais seguro em produção
jwt = JWTManager(app)

try:
    app.config['SWAGGER'] = {
        'openapi': '3.0.1'
    }

    swagger = Swagger(app, template_file='swagger.yaml')

except Exception:
    print("FALHA Swagger")

@app.route('/', methods=["GET"])
def index():
    """
    Root endpoint showing API version.

    Returns:
        str: Last update date
    """
    return "DATA ATUALIZAÇÃO 16-07-2024"


@app.route('/login', methods=['POST'])
def login():
    """
    Authenticate user and return JWT access token.

    Returns:
        JSON response with access_token or error message
    """
    login_info = request.authorization
    username = login_info['username']
    password = login_info['password']

    # Verifique se as credenciais são válidas
    for _, value in users.items():
        if (username == value["username"]) and (password == value["password"]):
            access_token = create_access_token(username)
            return jsonify({'access_token': access_token}), 200

    return jsonify({'error': 'Credenciais inválidas'}), 401


@app.route('/producao', methods=['GET'])
@jwt_required()
def producao():
    """
    Get wine and derivative production data.

    Query Parameters:
        ano (optional): Year or year range (e.g., 2021 or 1999-2023)

    Returns:
        JSON response with production data
    """
    link = {
        "Producao": "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02&"
    }

    json_data = my_request(link, ["Produto", "Quantidade (L.)"])
    return jsonify(json_data)


@app.route('/processamento', methods=['GET'])
@jwt_required()
def processamento():
    """
    Get grape processing data by type.

    Query Parameters:
        ano (optional): Year or year range (e.g., 2021 or 1999-2023)

    Returns:
        JSON response with processing data for different grape types
    """
    links = {
        "Processamento_Viníferas": (
            "http://vitibrasil.cnpuv.embrapa.br/index.php?"
            "subopcao=subopt_01&opcao=opt_03&"
        ),
        "Processamento_Americanas": (
            "http://vitibrasil.cnpuv.embrapa.br/index.php?"
            "subopcao=subopt_02&opcao=opt_03&"
        ),
        "Processamento_Uvas_De_Mesa": (
            "http://vitibrasil.cnpuv.embrapa.br/index.php?"
            "subopcao=subopt_03&opcao=opt_03&"
        ),
        "Sem_Classificacao": (
            "http://vitibrasil.cnpuv.embrapa.br/index.php?"
            "subopcao=subopt_04&opcao=opt_03&"
        )
    }

    json_data = my_request(links, ["Cultivar", "Quantidade (Kg)"])
    return jsonify(json_data)


@app.route('/comercializacao', methods=['GET'])
@jwt_required()
def comercializacao():
    """
    Get wine and derivative commercialization data.

    Query Parameters:
        ano (optional): Year or year range (e.g., 2021 or 1999-2023)

    Returns:
        JSON response with commercialization data
    """
    link = {
        "Comercializacao": (
            "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_04&"
        )
    }

    json_data = my_request(link, ["Produto", "Quantidade (L.)"])
    return jsonify(json_data)


@app.route('/importacao', methods=['GET'])
@jwt_required()
def importacao():
    """
    Get import data for wines, sparkling wines, grapes and juice.

    Query Parameters:
        ano (optional): Year or year range (e.g., 2021 or 1999-2023)

    Returns:
        JSON response with import data by country
    """
    links = {
        "Vinhos_De_Mesa": (
            "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_05&"
        ),
        "Espumantes": (
            "http://vitibrasil.cnpuv.embrapa.br/index.php?"
            "subopcao=subopt_02&opcao=opt_05&"
        ),
        "Uvas_Frescas": (
            "http://vitibrasil.cnpuv.embrapa.br/index.php?"
            "subopcao=subopt_03&opcao=opt_05&"
        ),
        "Uvas_Passas": (
            "http://vitibrasil.cnpuv.embrapa.br/index.php?"
            "subopcao=subopt_04&opcao=opt_05&"
        ),
        "Suco_De_Uva": (
            "http://vitibrasil.cnpuv.embrapa.br/index.php?"
            "subopcao=subopt_05&opcao=opt_05&"
        )
    }

    json_data = my_request(links, ["Países", "Quantidade (Kg)", "Valor (US$)"])
    return jsonify(json_data)


@app.route('/exportacao', methods=['GET'])
@jwt_required()
def exportacao():
    """
    Get export data for wines, sparkling wines, grapes and juice.

    Query Parameters:
        ano (optional): Year or year range (e.g., 2021 or 1999-2023)

    Returns:
        JSON response with export data by country
    """
    links = {
        "Vinhos_De_Mesa": (
            "http://vitibrasil.cnpuv.embrapa.br/index.php?"
            "subopcao=subopt_01&opcao=opt_06&"
        ),
        "Espumantes": (
            "http://vitibrasil.cnpuv.embrapa.br/index.php?"
            "subopcao=subopt_02&opcao=opt_06&"
        ),
        "Uvas_Frescas": (
            "http://vitibrasil.cnpuv.embrapa.br/index.php?"
            "subopcao=subopt_03&opcao=opt_06&"
        ),
        "Suco_De_Uva": (
            "http://vitibrasil.cnpuv.embrapa.br/index.php?"
            "subopcao=subopt_04&opcao=opt_06&"
        )
    }

    json_data = my_request(links, ["Países", "Quantidade (Kg)", "Valor (US$)"])
    return jsonify(json_data)


@app.errorhandler(InvalidParam)
def handle_bad_request(error):
    """Handle invalid parameter errors."""
    return jsonify({"error": str(error)}), 400


@app.errorhandler(CustomConnectionError)
def handle_internal_error(error):
    """Handle connection errors."""
    return jsonify({"error": str(error)}), 500


if __name__ == '__main__':
    app.run()
