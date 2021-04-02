import requests
import json
from requests.auth import HTTPDigestAuth

data = {
    "release_date":"2021-02-20",
    "artist":"Coldplay",
    "title":"Baggermuziek"
}

#headers = {'Authorization': 'Token '+ self.token.key, 'content_type':'application/json', 'Accept-Language' : 'en'}
#response = requests.post('http://127.0.0.1:8000/saveMeasure/', data=json.dumps(data), headers=headers)
p = requests.post('http://127.0.0.1:8000/restapi/releases/', data=data, auth=('ADMIN', 'ADMIN'))
#p = requests.get('http://127.0.0.1:8000/restapi/releases/', auth=('ADMIN', 'ADMIN'))
print(p)