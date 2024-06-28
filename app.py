from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from libs.users import users
import requests
from libs.transformationData import *


app = Flask(__name__)

# Configuração básica do JWT
app.config['JWT_SECRET_KEY'] = 'mykey'  # Troque para algo mais seguro em produção1
jwt = JWTManager(app)


@app.route('/',methods = ['POST'])
def index():
    return "GET INDEX, infomações"



@app.route('/login', methods=['POST'])
def login():

    loginInfo = request.authorization
    username = loginInfo['username']
    password = loginInfo['password']

    # Verifique se as credenciais são válidas (consulte seu banco de dados)
    
    for _ , value in users.items():

        if (username == value["username"]) and (password == value["password"]):
            access_token = create_access_token(username)
            return jsonify({'access_token': access_token}), 200
    
    return jsonify({'error': 'Credenciais inválidas'}), 401



@app.route('/producao', methods = ['POST'])
@jwt_required()
def producao():
    result = requests.get("http://vitibrasil.cnpuv.embrapa.br/download/Producao.csv")
    
    json_data = requestToJson(result) if result.status_code == 200\
        else csvToJson("Producao.csv")
        
    return jsonify(json_data)


@app.route('/processamento', methods = ['POST'])
@jwt_required()
def processamento():
    result = requests.get("http://vitibrasil.cnpuv.embrapa.br/download/ProcessaViniferas.csv")
    
    json_data = requestToJson(result) if result.status_code == 200\
        else csvToJson("Producao.csv")
        
    return jsonify(json_data)


@app.route('/comercializacao', methods = ['POST'])
@jwt_required()
def comercializacao():
    result = requests.get("http://vitibrasil.cnpuv.embrapa.br/download/Comercio.csv")
    
    json_data = requestToJson(result) if result.status_code == 200\
        else csvToJson("Comercio.csv")
        
    return jsonify(json_data)


@app.route('/importacao', methods = ['POST'])
@jwt_required()
def importacao():
    result = requests.get("http://vitibrasil.cnpuv.embrapa.br/download/ImpVinhos.csv")
    
    json_data = requestToJson(result) if result.status_code == 200\
        else csvToJson("ImpVinhos.csv")
        
    return jsonify(json_data)


@app.route('/expotacao', methods = ['POST'])
@jwt_required()
def expotacao():
    result = requests.get("http://vitibrasil.cnpuv.embrapa.br/download/ExpVinho.csv")
    
    json_data = requestToJson(result) if result.status_code == 200\
        else csvToJson("ExpVinho.csv")
        
    return jsonify(json_data)


app.run(host='0.0.0.0')