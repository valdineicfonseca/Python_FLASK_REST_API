# REST API CREATE DATABASE
# Definição de IP e Porta Server
# CREATE BD MySQL Database mysql_pythonbd
#----------------------------------------
# Author : Valdinei C @ 2022
#----------------------------------------

from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import json

#executado uma unica vez para criar banco de dados
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password=""
)

mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE mysql_pythonbd")
