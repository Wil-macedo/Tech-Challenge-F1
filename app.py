from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask import Flask, jsonify, request
from libs.users import users
from libs.requestFunction import myRequest


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


@app.route('/producao', methods = ['GET'])
@jwt_required()
def producao():
    
    link = {
        "Producao":"http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02&"
        }
    
    jsonData = myRequest(link, ["Produto", "Quantidade (L.)"])
    return jsonify(jsonData)


@app.route('/processamento', methods = ['GET'])
@jwt_required()
def processamento():

    links = {
        "Processamento_Viníferas ":f"http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_01&opcao=opt_03&",
        "Processamento_Americanas":f"http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_02&opcao=opt_03&",
        "Processamento_Uvas_De_Mesa":f"http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_03&opcao=opt_03&",
        "Sem_Classificacao":f"http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_04&opcao=opt_03&"
        }
    
    jsonData = myRequest(links, ["Cultivar", "Quantidade (Kg)"])
    return jsonify(jsonData)


@app.route('/comercializacao', methods = ['GET'])
@jwt_required()
def comercializacao():
    
    link = {
        "Comercializacao":"http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_04&"
        }
    
    jsonData = myRequest(link, ["Produto", "Quantidade (L.)"])
    return jsonify(jsonData)


@app.route('/importacao', methods = ['GET'])
@jwt_required()
def importacao():
    
    links = {
        "Vinhos_De_Mesa":f"http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_05&",
        "Espumantes":f"http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_02&opcao=opt_05&",
        "Uvas_Frescas":f"http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_03&opcao=opt_05&",
        "Uvas_Passas":f"http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_04&opcao=opt_05&",
        "Suco_De_Uva":f"http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_05&opcao=opt_05&"
        }
    
    jsonData = myRequest(links, ["Países", "Quantidade (Kg)", "Valor (US$)"])
    return jsonify(jsonData)


@app.route('/exportacao', methods = ['GET'])
@jwt_required()
def exportacao():

    links = {
        
        "Vinhos_De_Mesa":f"http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_01&opcao=opt_06&",
        "Espumantes":f"http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_02&opcao=opt_06&",
        "Uvas_Frescas":f"http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_03&opcao=opt_06&",
        "Suco_De_Uva":f"http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_04&opcao=opt_06&",
        }
 
    jsonData = myRequest(links, ["Países", "Quantidade (Kg)", "Valor (US$)"])
    return jsonify(jsonData)

app.run(host='0.0.0.0')