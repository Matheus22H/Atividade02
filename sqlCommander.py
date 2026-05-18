from env_loader import configs
import sqlite3, hashlib
class User:
    def __init__(self, username, password: str, nome, code=None):
        if code:
            self.code = code
        else:
            self.code = None
        self.username = username
        self.password = hashlib.sha256(password.encode()).hexdigest()
        self.nome = nome
    def dump(self):
        return (self.username, self.password, self.nome)
    def __repr__(self):
        if self.code:
            return f'{self.code=}, {self.username=}, {self.password=}, {self.nome=}'
        else:
            return f'{self.username=}, {self.password=}, {self.nome=}'
class MySQL(sqlite3.Connection):
    def __init__(self, database):
        super().__init__(database)
        self.database_loc = database
        self.Cursor = self.cursor()
        self.initializeDB()
    def initializeDB(self):
        self.execute("""CREATE TABLE IF NOT EXISTS usuarios (
            code            INTEGER PRIMARY KEY,
            username        TEXT    NOT     NULL,
            password        TEXT    NOT     NULL,
            nome            TEXT    NOT     NULL)""")
    def add(self, user: User):
        try: 
            self.Cursor.execute('INSERT INTO usuarios(username, password, nome) VALUES (?, ?, ?)', user.dump())
            self.commit()
            return 1
        except:
            print('Usuário já existe na Base de Dados')
            return 0
    def delete_all(self):
        try:
            with open(self.database_loc, 'w') as db:
                db.write('')
            self.initializeDB()
            return 1
        except:
            return 0
    def summarize_users(self):
        try:
            usuarios_carregados = [User(dado[1], dado[2], dado[3], code=dado[0]) for dado in self.Cursor.execute('SELECT * from usuarios').fetchall()]
            return usuarios_carregados
        except:
            return 0
    def verificar(self, usuario):
        'retorna TRUE para garantir...'
        try:
            dados = self.Cursor.execute('SELECT COUNT(*) FROM usuarios WHERE username=(?)', (usuario,)).fetchall()[0][0]
            if dados > 0:
                return True
            return False
        except:
            return True
            