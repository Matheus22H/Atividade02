from sqlCommander import User, MySQL
from main import *
from random import choice as rc
from hashlib import sha256
import pytest

def _genUserData():
    usernames1 = ['Ardiloso', 'Espuleta', 'Brincalhao', 'Bananao', 'Profissional', 'Gamer']
    usernames2 = ['Misterio', 'Ramon', 'Jose', 'Maria', 'Berenice', 'Atiradora']
    usernames3 = ['', '', 'Plus', '', '', 'Maximo']
    senha_extensoes = [c for c in '1234567890abcdef']
    nomes = ['Mathias', 'Joao', 'Carlos', 'Maria', 'Carlota', 'Carmen']
    username = rc(usernames1) + rc(usernames2) + rc(usernames3)
    passwhash = sha256(f'123456{rc(senha_extensoes)+rc(senha_extensoes)}'.encode()).hexdigest()
    nome = rc(nomes)
    return (username, passwhash, nome)
def test_create_x_users(x):
    db = MySQL('dev.db')
    for _ in range(x):
        db.add(User(*_genUserData()))
def test_create_100_users():
    test_create_x_users(100)
def test_create_1000_users():
    test_create_x_users(1000)
def test_input_right():
    pytest.MonkeyPatch.setattr('builtins.input', lambda: 'Carlos')
    assert inputer('Teste:') == "Carlos"