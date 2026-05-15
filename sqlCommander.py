from env_loader import configs
import sqlite3, hashlib
class User:
    def __init__(self, username, password, nome, code=None):
        if code:
            self.code = code
        self.username = username
        self.password = hashlib.sha256(password).hexdigest()
        self.nome = nome
    def dump(self):
        return (self.username, self.password, self.nome)

class MySQL(sqlite3.Connection):
    def __init__(self, database):
        super().__init__(database)
        self.database_loc = database
        self.Cursor = self.cursor()
    def initializeDB(self):
        self.execute("""CREATE TABLE IF NOT EXISTS usuarios (
            code            INTEGER PRIMARY KEY,
            username        TEXT    NOT     NULL,
            password        TEXT    NOT     NULL,
            nome            TEXT    NOT     NULL)""")
    def add(self, user: User):
        try: 
            self.Cursor.execute('INSERT INTO usuarios(username, password, nome) VALUES (?, ?, ?)', user.dump)
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
            usuarios_carregados = [User(dado[1], dado[2], dado[3], dado[0]) for dado in self.Cursor.execute('SELECT (code, username, password, nome) from usuarios').fetchall()]
            return usuarios_carregados
        except:
            return 0

            