import bcrypt
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
from database.conexao_mongodb import criaConexaoMongoDB
from database.inserir_dados import inserirDados, criaCadastro
from database.pesquisar_dados import puxar_configuracao, puxar_template, puxar_options, validaUser, validaEmail
from database.excluir_dados import excluirTemplate
from database.editar_dados import redefinirSenha
from functions.gerador import gerar, verificar_propiedade, concatenar

conexao = criaConexaoMongoDB()

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = '717g2tH6Y8jicHiNxEznJ4wapYG20QaD!@!@'
Session(app)

def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if 'email' in session:
            return view(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrapped_view

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/cadastro', methods=['POST', 'GET'])
def cadastro():
    email = request.form.get('email')
    senha = request.form.get('senha')
    confirma =  request.form.get('confirmar_senha')
    if email != None and senha != None and confirma != None:
        if validaEmail(conexao, email) == False:
            return render_template('cadastro.html', alerta='Email já cadastrado!')
        try:
            if senha == confirma:
                senha = senha.encode('utf-8')
                salt = bcrypt.gensalt()
                senha_hash = bcrypt.hashpw(senha, salt)
                cadastro = {
                    'email': email,
                    'senha': senha_hash
                }
                criaCadastro(conexao, cadastro)     
                return redirect(url_for('login'))
            else:
                return render_template('cadastro.html', alerta='Senhas não coincidem!')
        except:
            return render_template('cadastro.html', alerta='Senhas não coincidem!')
    return render_template('cadastro.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    email = request.form.get('email')
    senha = request.form.get('senha')
    if email != None and senha != None:
        resultado = validaUser(conexao, email)
        try:
            if resultado["email"] == email and bcrypt.checkpw(senha.encode('utf-8'), resultado["senha"]):
                session['email'] = resultado['email']
                return redirect(url_for('lobby'))
            else:
                return render_template('login.html', alerta='Usuário ou senha incorretos!')
        except:
            return render_template('login.html', alerta='Ocorreu um erro durante o login.')
    return render_template('login.html') 

@app.route('/redefinir_senha', methods=['GET', 'POST'])
@login_required
def redefinir_senha():
    senha = request.form.get('senha')
    confirma = request.form.get('confirmar_senha')
    if senha != None and confirma != None:
        if senha == confirma:
            senha = senha.encode('utf-8')
            salt = bcrypt.gensalt()
            senha_hash = bcrypt.hashpw(senha, salt)
            redefinir = {
                'email': session['email'],
                'senha': senha_hash
            }
            redefinirSenha(conexao, redefinir)
            return redirect(url_for('sucesso'))
        else:
            return render_template('redefinir_senha.html', alerta='Senhas não coincidem!')
    return render_template('redefinir_senha.html')

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('login'))

@app.route('/sobre', methods=['POST', 'GET'])
def sobre():
    return render_template('Sobre.html')
    
@app.route('/lobby', methods=['POST', 'GET'])
@login_required
def lobby():
    try:
        if request.method == 'POST' or request.method == 'GET':
            enviar = request.form.get('enviar')
            nome_template = request.form.get('nome_template')
            if nome_template != None:
                return redirect('/lobby/' + nome_template)
            if ((request.form.getlist('propiedade') != []) and (enviar == 'Criar')):
                configuracao = {
                    'tipo_template': request.form.get('equipamento'),
                    'propiedade': ','.join(request.form.getlist('propiedade')),
                    'nome_template': str(request.form.get('nome')),
                    'autor': session['email']
                }
                inserirDados(conexao, configuracao)
                return redirect(url_for('sucesso'))
            elif (request.form.getlist('propiedade') == []) and (enviar != 'Criar'):
                return render_template('lobby.html')
            else:
                return render_template('lobby.html', alerta='Error: Propiedades não foram selecionadas!!')
        return render_template('lobby.html')
    except:
        return render_template('lobby.html', alerta='Erro ao inserir dados!')
        
@app.route('/lobby/<nome_template>', methods=['POST', 'GET'])
@login_required
def gerador(nome_template):
    valores = {
        'gerencia': request.form.get('gerencia'),
        'gerencia_network': concatenar(request.form.get('gerencia_network'), request.form.get('gerencia_barramento')),
        'valido': request.form.get('valido'),
        'nomenclatura': request.form.get('nomenclatura'),
        'queue': request.form.get('queue'),
        'interna_network': concatenar(request.form.get('interna_network'),request.form.get('queue_barramento'))   
    }    
    resultado = puxar_configuracao(conexao, nome_template)
    propriedades = resultado[0]["propiedade"].strip().split(',')
    display_propriedades = verificar_propiedade(propriedades)
    validador = request.form.get('validador')
    if validador == 'Gerar':
        codigos = gerar(puxar_template(conexao, resultado[0]["tipo_template"]), propriedades, valores)
        return render_template('codigo.html', 
            codigos=codigos)
    return render_template('gerador.html', 
        propriedades=propriedades, 
        display_propriedades=display_propriedades,  
        nome_template=nome_template)
    
@app.route('/templates', methods=['POST', 'GET'])
@login_required
def templates():
    templates = puxar_options(conexao, session['email'])
    print(templates)
    return render_template('templates.html', templates=templates)

@app.route('/sucesso', methods=['GET'])
@login_required
def sucesso():
    return render_template('sucesso.html')

@app.route('/excluir', methods=['GET', 'POST'])
@login_required
def excluir():
    templates = puxar_options(conexao)
    return render_template('excluir.html', templates=templates)

@app.route('/excluir/<nome_template>', methods=['GET'])
def excluir_template(nome_template):
    excluir = {
        'nome_template': nome_template
    }
    excluirTemplate(conexao, excluir)
    return redirect(url_for('excluir'))


if __name__ == '__main__':
    app.run(debug=True)