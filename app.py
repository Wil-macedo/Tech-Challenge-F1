from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from users import users
import requests
import json
import pandas as pd
from io import StringIO
import os

app = Flask(__name__)

# Configuração básica do JWT
app.config['JWT_SECRET_KEY'] = 'mykey'  # Troque para algo mais seguro em produção1
jwt = JWTManager(app)

@app.route('/',methods = ['POST'])
def index():
    return "GET INDEX, infomações"


@app.route('/login', methods=['POST'])
def login():

    loginInfo = request.authorization.parameters
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
    
    if result.status_code == 200 and 1 !=1:  # OK, site OK
        csvInfo = result.text.split('\n')
    else:  # LEITURA DO CSV.
        csvFile = os.path.join(os.path.abspath("."),"csvFiles", "Producao.csv")
        csvInfo = pd.read_csv(StringIO(csvFile), sep=';', encoding='ISO-8859-1')




    csvInfo = result.text.split('\n')


    headers = csvInfo[0].split(';')

    # Processando os dados e convertendo para JSON
    data = []
    for line in csvInfo[1:]:
        if line:  # Ignorar linhas vazias
            values = line.split(';')
            entry = {headers[i]: values[i].encode('ISO-8859-1').decode('utf-8', 'ignore') for i in range(len(headers))}
            data.append(entry)
        
    json_data = json.dumps(data, ensure_ascii=False)





    return jsonify(json_data)

@app.route('/processamento', methods = ['POST'])
@jwt_required()
def processamento():
    return 'Endpoint processamento'


@app.route('/comercializacao', methods = ['POST'])
@jwt_required()
def comercializacao():
    request.ge
    return 'Endpoint comercializacao'


@app.route('/importacao', methods = ['POST'])
@jwt_required()
def importacao():
    return 'Enpoint importacao'


@app.route('/expotacao', methods = ['POST'])
@jwt_required()
def expotacao():
    return 'Endpoint expotacao'


app.run(host='0.0.0.0')