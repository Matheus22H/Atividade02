import json
configs = {}
try:
    with open('.env', 'r', encoding='utf-8') as env:
        __data = env.read()
        try: 
            configs: dict = json.loads(__data)
        except:
            configs = {}
except:
    configs = {}
    with open('.env', 'x'):
        pass