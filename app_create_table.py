# REST API CREATE TABLE
# Definição de IP e Porta Server
# CREATE Table MySQL in Database mysql_pythonbd
#----------------------------------------
# Author : Valdinei C @ 2022
#----------------------------------------

from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import json

#antes executar app_create_bd uma unica vez
#conexao com bd 
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/mysql_pythonbd'

# Criar classe Usuario db.Model pelo terminal
# Abrir terminal digitar:
# python
# cirando tabelas pelo terminal uma unica vez.
# from app_create import db
# db.create_all()
db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    nome = db.Column(db.String(50))
    email = db.Column(db.String(100))
