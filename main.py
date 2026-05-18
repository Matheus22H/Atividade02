import random, hashlib
from sqlCommander import MySQL, User
from env_loader import configs

saudacoes = [
    'Olá usuário! Preciso te conhecer melhor, poderia me dar algumas informações?',
    '*Um usuário selvagem apareceu...*',
    'Quem é você?',
    'Eu conheço você de algum lugar...?',
    'Saudações guerreiro!',
    'Eae, gostaria de adentrar no sistema?',
    'Ouvi boatos sobre você, mas com esse ar misterioso? Afinal, quem é você de verdade?',
    'deletar C:/SistemaWindows/ Acesso negado... Inicalizando Hack.\nBrincadeira, e aí aluno!'
]
def inputer(frase, tamanho=3, proibidos = []):
    'Ele só vai sair daqui SE o tamanho do que você digitou foi igual ou maior a variavel tamanho, SENÃO ele vai ficar indeterminadamente repetindo'
    _temp = input(frase)
    if len(proibidos) == 0:
        proibidos = []
    for item in proibidos:
        if item in _temp:
            print(f'Valor inválido, ele contém um caractére proíbido! ({item})')
            return inputer(frase, tamanho)
    if len(_temp) >= tamanho:
        return _temp
    else:
        print('Valor inválido, preciso de no mínimo o tamanho igual ou maior a', tamanho)
        return inputer(frase, tamanho)
def input_safe(frase):
    _temp = input(frase)
    if _temp.isnumeric():
        return _temp
    else:
        print('Foi solicitado NUMERO!')
        return input_safe(frase)
def saudacao():
    print(random.choice(saudacoes))
    
def coletar_usuario():
    username = inputer("Insira seu nome de usuário: ", proibidos='!@#$%&*()_+=-[]{()} ')
    return username

def coletar_senha():
    password_hash = hashlib.sha256(inputer("Shhhh... Insira sua senha: ", tamanho=8).encode()).hexdigest()
    return password_hash

def coletar_nome():
    nome = inputer('Hmmm. E seu nome, qual seria? ')
    return nome

def inicializar():
    'ele CRIA a intância do gerenciador de database'
    global _database
    _database = MySQL('./dev.db')

def usuario_existe(username):
    'Verifica se o username existe'
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

def normal():
    global username
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

def get_adm():
    print('- ADMINISTRATIVO -')
    print('- Funções:')
    funcs = ['Sair', 'Desabilitar ADM', 'Pegar todos os usuários', 'Usar normalmente', 'Deletar tudo!']
    for func in enumerate(funcs, start=1):
        print(f'{func[0]}.', func[1])
    match int(input_safe('Selecione tua opção (use números): ')):
        case 1:
            exit()
        case 2:
            with open('.env', 'w') as f:
                f.write('{"admin":false}')
            exit()
        case 3:
            if len([print(i) for i in _database.summarize_users()]) == 0:
                print('Não tinha usuários...')
        case 4:
            normal()
        case 5:
            print('Deletando tudo :< seu sem coração!!!')
            _database.delete_all()
        case _:
            print('--- QUÊ????????!!')
            get_adm()

def main():
    inicializar()
    if configs.get('admin', False):
        get_adm()    
    else:
        normal()
        
try:
    main()
except KeyboardInterrupt:
    print('\n\nFinalizado por Ctrl+C')