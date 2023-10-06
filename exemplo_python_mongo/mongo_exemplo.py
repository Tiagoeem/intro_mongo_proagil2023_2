import pymongo

# Conectando ao servidor local do MongoDB
str_con = "mongodb+srv://admin:admin@projagil.vwwy9el.mongodb.net/?retryWrites=true&w=majority"
client_con = pymongo.MongoClient(str_con)

# selecionei o banco de dados e a collection
pacientes_col = client_con.db_clinica.pacientes

# filtar os dados
resultados = pacientes_col.find()
lista_resultados = list(resultados)
print("Todos os pacientes")
print(lista_resultados)

filter_ = {
    "idade": {"$gt": 30}
}
projection_ = {}
resultados = pacientes_col.find(filter_, projection_)
lista_resultados = list(resultados)
print("Todos os pacientes - Filtrado")
print(lista_resultados)


filter_ = {
    "idade": {"$gt": 30}
}
projection_ = {}
resultado = pacientes_col.find_one(filter_, projection_)
print("\nUM paciente- Filtrado")
print(resultado)