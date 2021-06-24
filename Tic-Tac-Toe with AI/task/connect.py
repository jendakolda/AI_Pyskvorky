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
url = 'https://piskvorky.jobs.cz/api/v1/connect'
headers = CaseInsensitiveDict()
headers['accept'] = 'application/json'
headers['Content-Type'] = 'application/json'
data = "{ \"nickname\": \"DoktorPyskvor\", \"userToken\": \"95989a37-418c-4fcc-b9f7-0160d529753d\"}"
response = requests.post(url, headers=headers, data=data)
# print(response.headers)
# print(response.status_code)
dictionary = dict()
dictionary.loads(response.json())
print(json.dumps(response.json(), indent=4))
print(dictionary['gameId'])

