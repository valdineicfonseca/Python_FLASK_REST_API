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
#----------------------------------
# Author : Valdinei C @ 2022
#----------------------------------

############################
#!/usr/bin/env python
# funcao def pegaValor

import html
import cgi
import cgitb; cgitb.enable()     # for troubleshooting

############################


from pickle import TRUE
from flask import Flask, Response, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import json

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

    #transformar objeto em json
    def to_json(self):
        return {"id": self.id, "nome": self.nome, "email": self.email}

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
    ##form = cgi.FieldStorage()
    ##say  = html.escape(form["say"])
    ##print(say)
    print("TESTE.....",nome_captura," ",email_captura)
    
    try:
        usuario = Usuario(nome=nome_captura, email= email_captura)
        db.session.add(usuario)
        db.session.commit()
        return gera_response(201, "usuario", usuario.to_json(), "Criado com sucesso")
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


app.run(host="127.0.0.1", port=81)