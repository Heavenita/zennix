def excluirTemplate(conexao, excluir):
    collection = conexao["configuracao"]
    collection.delete_one({"nome_template": excluir['nome_template']})