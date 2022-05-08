# REST API Consulta
# Definição de IP e Porta Server
# Conexao BD MySQL Database mysql_pythonbd
# Table usuarios
# Return all users
# [GET] http://127.0.0.1:81/users
#----------------------------------
# Author : Valdinei C @ 2022
#----------------------------------

from pickle import TRUE
from re import U
from urllib import response
from flask import Flask, Response, request
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
    return 'Web app Flask API Consult <br><br> Method: [GET] <a href=\"http://127.0.0.1:81/users\">http://127.0.0.1:81/users</a>'


# Selecionar Tudo
@app.route("/users", methods=["GET"])
def seleciona_usuarios():
    usuarios_objetos = Usuario.query.all()
    usuarios_json = [usuario.to_json() for usuario in usuarios_objetos]
    print(usuarios_objetos)
    print(usuarios_json)
    #return gera_response(200, "usuarios", usuarios_json)
    return Response(json.dumps(usuarios_json))

app.run(host="127.0.0.1", port=81)