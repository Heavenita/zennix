def puxar_configuracao(conexao, nome_template):
    collection = conexao["configuracao"]
    document = {"nome_template": nome_template}
    resultado = collection.find(document)
    return resultado
    

def puxar_template(conexao, nome_template):
    collection = conexao["template"]
    document = {"nome_template": nome_template}
    resultado = collection.find(document)
    resultado = resultado[0]["codigo_template"]
    resultado = resultado.strip().split('/') and resultado.strip().split('\n')
    return resultado

def puxar_options(conexao, email):
    collection = conexao["configuracao"]
    document = {"autor": email}
    resultado = collection.find(document)
    concatenado = []
    for i in resultado:
        concatenado.append(i["nome_template"])
    return concatenado

def validaUser(conexao, email):
    collection = conexao["cadastro"]
    document = {"email": email}
    resultado = collection.find_one(document)
    return resultado

def validaEmail(conexao, email):
    collection = conexao["cadastro"]
    document = {"email": email}
    resultado = collection.find_one(document)
    if resultado == None:
        return True
    return False