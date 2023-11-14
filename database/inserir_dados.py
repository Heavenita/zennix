def inserirDados(conexao, configuracao):
    collection = conexao["configuracao"]
    document = {"tipo_template": configuracao['tipo_template'], "propiedade": configuracao['propiedade'], "nome_template": configuracao['nome_template'], "autor": configuracao['autor']}
    collection.insert_one(document)
    

def criaCadastro(conexao, cadastro):
    collection = conexao["cadastro"]
    document = {"email": cadastro['email'], "senha": cadastro['senha']}
    collection.insert_one(document)

