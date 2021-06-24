import json
import requests
from requests.structures import CaseInsensitiveDict

# to get an initial game token
# url = 'https://piskvorky.jobs.cz/api/v1/user'
# headers = CaseInsensitiveDict()
# headers['accept'] = 'application/json'
# headers['Content-Type'] = 'application/json'
# data = "{ \"nickname\": \"DoktorPyskvor\", \"email\": \"kolda@pm.me\"}"
# response = requests.post(url, headers=headers, data=data)
# print(response.text)


# to start a game
class API_connect:
    def __init__(self):
        self.user = dict()
        self.user['userId'] = 'a444df7d-3c49-4188-bddb-7a8720ad7a8'
        self.user['userToken'] = '95989a37-418c-4fcc-b9f7-0160d529753d'
        self.user['nickname'] = 'DoktorPyskvor'
        self.address = 'https://piskvorky.jobs.cz/api/v1/'
        self.game_token = str()


    def connect(self):
        url = self.address + 'connect'
        headers = CaseInsensitiveDict()
        headers['accept'] = 'application/json'
        headers['Content-Type'] = 'application/json'
        token = self.user['userToken']
        data = f'{{"userToken": "{token}"}}'
        response = requests.post(url, headers=headers, data=data)
        print(response.status_code)

        dictionary = response.json()
        self.game_token = response.json()['gameToken']
        print(json.dumps(response.json(), indent=4))

    def play(self, play_x=0, play_y=0):
        url = self.address + 'play'
        headers = CaseInsensitiveDict()
        headers['accept'] = 'application/json'
        headers['Content-Type'] = 'application/json'
        data = dict()
        data["userToken"] = self.user['userToken']
        data["gameToken"] = self.game_token
        data["positionX"] = play_x
        data["positionY"] = play_y

        response = requests.post(url, headers=headers, data=json.dumps(data))
        print(response.json())


print(API_connect().user)
a = API_connect()
a.connect()
a.play(0, 0)




