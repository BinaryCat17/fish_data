import yadisk
import json
from os import path


class Serializer:
    def __init__(self):
        # токен отсюда https://oauth.yandex.ru/authorize?response_type=token&client_id=ТутВашАйди
        userhome = path.expanduser('~')
        token_file = open(path.join(userhome, '.fish/yadisk.json'))
        cfg = json.load(token_file)
        self.y = yadisk.YaDisk(cfg['id'], cfg['secret'], cfg['token'])

    def save(self, filename):
        self.y.upload(filename, f'/FishMl/{filename}')
