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
def inputer(frase, tamanho=3):
    _temp = input(frase)
    if len(_temp) >= tamanho:
        return _temp
    else:
        print('Valor inválido, preciso de no mínimo o tamanho igual ou maior a', tamanho)
        return inputer(frase, tamanho)

def saudacao():
    print(random.choice(saudacoes))
    
def coletar_usuario():
    username = inputer("Insira seu nome de usuário: ")
    return username
def coletar_senha():
    password_hash = hashlib.sha256(inputer("Shhhh... Insira sua senha: ", tamanho=8).encode()).hexdigest()
    return password_hash
def coletar_nome():
    nome = inputer('Hmmm. E seu nome, qual seria? ')
    return nome
def inicializar():
    global _database
    _database = MySQL('./db.db')

def usuario_existe(username):
    return _database.verificar(username)

def cadastrar_se():
    global username
    username = coletar_usuario()
    if usuario_existe(username):
        print('DEV')
        return False
    return True
def criar_usuario(usuario_montado: User):
    data = _database.add(usuario_montado)
    return bool(data)
def main():
    global username
    inicializar()
    saudacao()
    sucesso = cadastrar_se()
    while not sucesso:
        print('Ops... usuário já existente, poderia por favor tentar algo mais criativo? ')
        sucesso = cadastrar_se()
    password_hash = coletar_senha()
    nome = coletar_nome()
    usuario_montado = User(username, password_hash, nome)
    if not criar_usuario(usuario_montado):
        print('Ocorreu um erro :( tente novamente...')
    else:
        print(f'AEEEE! Bem vindo {username}... ou melhor seria {nome}?')
main()