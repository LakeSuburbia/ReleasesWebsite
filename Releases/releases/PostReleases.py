import requests

data = {
    "release_date":"2021-02-20",
    "artist":"Coldplay",
    "title":"Baggermuziek"
}

req = requests.post('http://127.0.0.1:8000/restapi/releases/', data, auth=('ADMIN', 'ADMIN'))

print(req)