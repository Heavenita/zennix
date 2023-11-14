def redefinirSenha(conexao, redefinir):
    collection = conexao["cadastro"]
    collection.update_one({"email": redefinir['email']}, {"$set": {"senha": redefinir['senha']}})