# REST API CRUD
# Definição de IP e Porta Server
# Conexao BD MySQL Database mysql_pythonbd
# Table usuarios
# + Return all users
#   [GET] http://127.0.0.1:81/usuarios
#
# + Add user
#   [POST] http://127.0.0.1:81/usuario
#   BODY
#   JSON
#{
#    "nome": "NomeDoUsuario",
#    "email": "emaildousuario@email.com"
#}
#-------------------------------------
# Author : Valdinei C @ 2022 | Develop
#-------------------------------------

from email import encoders
from email.mime.base import MIMEBase
from pickle import TRUE
import smtplib
from flask import Flask, Response, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import json

from email_senha import EMAIL_MENSAGEM

# antes executar app_create_db, criar database unica vez.
# executar app_create_table, criar tabela unica vez.
# Padrao utilizado variavel app mas caso utilize outro nome colcoar a mesma variavel em todo arquivo.
# variavel app nao tem relaçao com nome do arquivo.
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@127.0.0.1/mysql_pythonbd'

if __name__ == '__main__':
    app.debug = TRUE

db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    nome = db.Column(db.String(50))
    email = db.Column(db.String(100))
    seo = db.Column(db.String(10))
    ia = db.Column(db.String(10))
    vendas = db.Column(db.String(10))
    tp = db.Column(db.String(10))
    data_cadastro = db.Column(db.String(20))

    #transformar objeto em json
    def to_json(self):
        return {"id": self.id, "nome": self.nome, "email": self.email, "seo": self.seo, "ia": self.ia, "vendas": self.vendas, "tp": self.tp, "data_cadastro":self.data_cadastro}

#rota para raiz 
@app.route('/')
def index():
    return 'Web app Flask(Python) RESTfull API CRUD <br><a href="http://127.0.0.1:81/apidocumentacao">API Documentation</a> <br><br>Consulta todos usuários <br> Method: [GET] <a href=\"http://127.0.0.1:81/usuarios\">http://127.0.0.1:81/usuarios</a> <br><br> <i>Dev: Valdinei C. @ 2022<i/>'

#rota documatarion api
@app.route('/apidocumentacao')
def apidoc():
    return render_template('index.html')

# Verifica email de usuarios cadastrados, caso não cadastrado aparece form
@app.route("/verifica/<email_user>", methods=["GET"])
def seleciona_usuarios_verifica(email_user):
    usuarios_objetos = Usuario.query.all()
    
    # Loop for todos usuarios objetos convertidos em lista JSON
    usuarios_json = [usuario.to_json() for usuario in usuarios_objetos]
    print(usuarios_objetos)
    
    cad = "Cadastre seu e-mail"

    # imprime e-mail de todos usuarios
    for  usr_json in usuarios_json:
        if email_user == usr_json["email"]:
            cad = "E-mail já cadastrado"
            print(cad)
        print(usr_json["email"])

    return render_template('verifica_form.html', name=email_user, cadastro=cad)


#teste pegar valor
@app.route("/pegavalor", methods=['GET', 'POST'])
def pegaValor():
    ##print("Content-Type: text/html") # HTTP header to say HTML is following
    ##print()                          # blank line, end of headers
    nome_captura = request.form['nome_form']
    email_captura = request.form['email_form']
    seo_captura = request.form['seo_form']
    ia_captura = request.form['ia_form']
    vendas_captura = request.form['vendas_form']
    tp_captura = request.form['tp_form']
    data_captura = request.form['data_form']
    ##form = cgi.FieldStorage()
    ##say  = html.escape(form["say"])
    ##print(say)
    print("Cliente.....",nome_captura," ",email_captura)
    print("S.E.O ", seo_captura)
    print("Inteligencia Artificial ", ia_captura)
    print("Vendas na internet ", vendas_captura)
    print("Trafego Pago ", tp_captura)
    print("Data de registo ", data_captura)
    
    try:
        usuario = Usuario(nome=nome_captura, email= email_captura, seo=seo_captura, ia=ia_captura, vendas=vendas_captura, tp=tp_captura, data_cadastro=data_captura)
        db.session.add(usuario)
        db.session.commit()
        return envia_email(email_captura)
        #return gera_response(201, "usuario", usuario.to_json(), "Criado com sucesso")
    except Exception as e:
        print('Erro', e)
        return gera_response(400, "usuario", {}, "Erro ao cadastrar")
    
    #return render_template('index.html', name=nome_captura, email_cap=email_captura)


# Selecionar Tudo
@app.route("/usuarios", methods=["GET"])
def seleciona_usuarios():
    usuarios_objetos = Usuario.query.all()
    
    # Loop for todos usuarios objetos convertidos em lista JSON
    usuarios_json = [usuario.to_json() for usuario in usuarios_objetos]
    print(usuarios_objetos)
    
    for  usr_json in usuarios_json:
        print(usr_json["email"])

    return gera_response(200, "usuarios", usuarios_json, "Retorna todos os usuarios")

# Selecionar Individual
@app.route("/usuario/<id>", methods=["GET"])
def seleciona_usuario(id):
    usuario_objeto = Usuario.query.filter_by(id=id).first()
    usuario_json = usuario_objeto.to_json()

    return gera_response(200, "usuario", usuario_json)

# Cadastrar usuario
@app.route("/usuario", methods=["POST"])
def cria_usuario():
    body = request.get_json()

    try:
        usuario = Usuario(nome=body["nome"], email= body["email"])
        db.session.add(usuario)
        db.session.commit()
        return gera_response(201, "usuario", usuario.to_json(), "Criado com sucesso")
    except Exception as e:
        print('Erro', e)
        return gera_response(400, "usuario", {}, "Erro ao cadastrar")


# Atualizar
@app.route("/usuario/<id>", methods=["PUT"])
def atualiza_usuario(id):
    usuario_objeto = Usuario.query.filter_by(id=id).first()
    body = request.get_json()

    try:
        if('nome' in body):
            usuario_objeto.nome = body['nome']
        if('email' in body):
            usuario_objeto.email = body['email']
        
        db.session.add(usuario_objeto)
        db.session.commit()
        return gera_response(200, "usuario", usuario_objeto.to_json(), "Atualizado com sucesso")
    except Exception as e:
        print('Erro', e)
        return gera_response(400, "usuario", {}, "Erro ao atualizar")

# Deletar
@app.route("/usuario/<id>", methods=["DELETE"])
def deleta_usuario(id):
    usuario_objeto = Usuario.query.filter_by(id=id).first()

    try:
        db.session.delete(usuario_objeto)
        db.session.commit()
        return gera_response(200, "usuario", usuario_objeto.to_json(), "Deletado com sucesso")
    except Exception as e:
        print('Erro', e)
        return gera_response(400, "usuario", {}, "Erro ao deletar")

#Função response padronizada com status, nome_conteudo, conteudo e mensagem opcional
def gera_response(status, nome_do_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_do_conteudo] = conteudo

    if(mensagem):
        body["mensagem"] = mensagem

    return Response(json.dumps(body), status=status, mimetype="application/json")






# Envio de e-mail automatico - opção google security app menos seguro ativada
@app.route("/envia/email/<email_send>", methods=["GET"])
def envia_email(email_send):
    # Importa passowrd de outro arquivo.
    from email_senha import EMAIL_PASSWORD as EMAIL_PASS
    
    # Import libs e multpart
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    EMAIL_ADDRESS="magodigital.email.automatico@gmail.com"

    # start servidor SMTP
    host ="smtp.gmail.com"
    email_port = "587"
    login = EMAIL_ADDRESS
    senha = EMAIL_PASS

    server = smtplib.SMTP(host,email_port)
    server.ehlo()
    server.starttls()
    server.login(login,senha)

    # Construindo estrutura do e-mail
    conteudo_email = EMAIL_MENSAGEM

    email_msg = MIMEMultipart()
    email_msg['From'] = login
    email_msg['To'] = email_send
    email_msg['Subject'] = "Aprenda a escalar suas vendas - MAGO-DIGITAL [[[Mensagem Automática]]] "
    email_msg.attach(MIMEText(conteudo_email,'html'))

    # para colocar arquivo anexo - leitura em binario
    #file_anexo = "e:\\temp\\teste.txt"
    #attachment = open(file_anexo,'rb') # R read B binario - leitura de arquivo em binario
    
    #transformando arquivo de Binario para Base64
    #att = MIMEBase('application', 'octet-stream')
    #att.set_payload(attachment.read())
    #encoders.encode_base64(att)

    # Cabeçalho do E-mail
    #att.add_header('Content-Disposition', f'attachment; filename=teste.txt')
    #attachment.close() # Fecha o arquivo

    # Envia e-mail no tipo MIME no Servidor SMTP
    server.sendmail(email_msg["From"],email_msg["To"],email_msg.as_string())
    server.quit() ### Fecha conexao...

    return render_template('verifica_form.html', name=email_send, cadastro='E-mail já cadastrado')

# Roda aplicação ip local e porta
app.run(host="127.0.0.1", port=81)