from pymongo import MongoClient

def criaConexaoMongoDB():
    try:
        client = MongoClient("mongodb+srv://zennix:zennix445196@zennix.1nkqx2s.mongodb.net")
        print("Conexão com o banco de dados realizada com sucesso!")
        return client["zennix"]
    except Exception as erro:
        print("Ocorreu algum erro na conexao")
