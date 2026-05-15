import json
def load():
    global configs
    with open('.env', 'r', encoding='utf-8') as env:
        __data = env.read()
        try: 
            configs: dict = json.loads(__data)
        except:
            configs = {}
load()