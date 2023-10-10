from flask import Flask, jsonify, request
from flask_pymongo import PyMongo, ObjectId
from credentials_file import settings, credenciais

app = Flask(__name__)
app.config["MONGO_URI"] = f"mongodb+srv://{credenciais['user_mongo']}:{credenciais['password_mongo']}@{settings['host']}/{settings['database']}?retryWrites=true&w=majority"
mongo = PyMongo(app)

# rota de teste de funcionamento da API
@app.route('/')
def index():
    return {"mensagem": "Api em funcionamento"}, 200

# Cadastro de pacientes
@app.route('/pacientes', methods=['POST'])
def create_paciente():
    try:
        data = request.json
        if not all(k in data for k in ("nome_paciente", "idade", "cpf")):
            return jsonify({"erro": "Campos obrigatórios faltando!"}), 400

        paciente_id = mongo.db.pacientes.insert_one(data)
        print(paciente_id.inserted_id)
        return {"_id": str(paciente_id.inserted_id)}, 201
    except Exception as e:
        return {"erro":str(e)}, 500


# leitura de pacientes
@app.route('/pacientes', methods=['GET'])
def get_pacientes():
    try:
        filter_ = {}
        projection_ = {}
        pacientes = list(mongo.db.pacientes.find(filter_, projection_))
        for paciente in pacientes:
            paciente["_id"] = str(paciente["_id"])
        return {"pacientes": pacientes}, 200
    except Exception as e:
        return {"erro":str(e)}, 500
    

# leitura de um paciente especifico
@app.route('/pacientes/<paciente_id>', methods=['GET'])
def get_paciente(paciente_id):
    try:
        # ObjectId é uma classe do pymongo que serve para validar o id do mongo
        paciente = mongo.db.pacientes.find_one({"_id": ObjectId(paciente_id)})
        if paciente:
            paciente["_id"] = str(paciente["_id"])
            return paciente, 200
        return jsonify({"erro": "Paciente não encontrado!"}), 404
    except Exception as e:
        return {"erro":str(e)}, 500


# Atualização de um paciente
@app.route('/pacientes/<paciente_id>', methods=['PUT'])
def update_paciente(paciente_id):
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Dado para atualização não fornecido!"}), 400
        mongo.db.pacientes.update_one({"_id": ObjectId(paciente_id)}, {"$set": data})
        return jsonify({"message": f"Paciente {paciente_id} atualizado com sucesso!"}), 200
    except Exception as e:
        return {"erro":str(e)}, 500



if __name__ == '__main__':
    app.run(debug=True, threaded=True)
