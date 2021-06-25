import json
from time import sleep

import requests


# to get an initial game token
# def start_game():
#     url = 'https://piskvorky.jobs.cz/api/v1/user'
#     headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
#     data = {"nickname": "frantanovak", "email": "franta@pm.me"}
#     response = requests.post(url, headers=headers, data=json.dumps(data))
#     print(json.dumps(response.json(), indent=4))


# to start a game
class API_Connect:
    def __init__(self):
        self.headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
        self.user = {'userId': 'a444df7d-3c49-4188-bddb-7a8720ad7a8',
                     'userToken': '95989a37-418c-4fcc-b9f7-0160d529753d',
                     'nickname': 'DoktorPyskvor', }
        self.address = 'https://piskvorky.jobs.cz/api/v1/'
        self.game_token = str()

    def connect(self):
        url = self.address + 'connect'
        data = {'userToken': self.user['userToken']}
        response = requests.post(url, headers=self.headers, data=json.dumps(data))
        self.game_token = response.json()['gameToken']

    def play(self, play_x=0, play_y=0):
        url = self.address + 'play'

        data = {"userToken": self.user['userToken'],
                "gameToken": self.game_token,
                "positionX": play_x,
                "positionY": play_y, }

        response = requests.post(url, headers=self.headers, data=json.dumps(data))
        print(json.dumps(response.json(), indent=4))
        print(self.game_token)
        return response.status_code

    def check_status(self):
        url = self.address + 'checkStatus'
        data = {'userToken': self.user['userToken'], 'gameToken': self.game_token}
        response = requests.post(url, headers=self.headers, data=json.dumps(data))
        print(json.dumps(response.json(), indent=4))

    def check_last_status(self):
        url = self.address + 'checkLastStatus'
        data = {'userToken': self.user['userToken'], 'gameToken': self.game_token}
        response = requests.post(url, headers=self.headers, data=json.dumps(data))
        print(json.dumps(response.json(), indent=4))


a = API_Connect()
a.connect()
a.check_status()
while True:
    x = int(input('x'))
    y = int(input('y'))
    status = a.play(x, y)
    if status == 201:
        print('Coordinates were saved')
    elif status == 226:
        print('The game has been completed')
        break
    elif status == 400:
        print('invalid request')
    elif status == 401:
        print('invalid user or token')
    elif status == 406:
        print('its the second player\'s turn')
        sleep(20)
    elif status == 410:
        while status == 410:
            print('waiting for a player to join')
            sleep(20)
            status = a.play(x, y)

# start_game()
