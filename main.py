import random, hashlib
from sqlCommander import MySQL, User
saudacoes = [
    'Olá usuário! Preciso te conhecer melhor, poderia me dar algumas informações?',
    '*Um usuário selvagem apareceu...*',
    'Quem é você?',
    'Eu conheço você de algum lugar...?',
    'Saudações guerreiro!',
    'Eae, gostaria de adentrar no sistema?'
]

def saudacao():
    print(random.choice(saudacoes))

def inicializar():
    global _database
    _database = MySQL('./db.db')
