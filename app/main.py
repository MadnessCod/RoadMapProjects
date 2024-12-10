import requests
import json


from local_settings import API_KEY


key = API_KEY
location = input('Enter location: \nshema:\n{\nLondon,UK\nlongitude,latitude\n}\nEnter Here: ')

while location.find(',') == -1:
    print('Your entry doesn\'t have comma')
    location = input('Enter location: \nlongitude,latitude\nEnter Here: ')

print('Retrieving data...')

base_url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}?key={key}'

try:
    response = requests.get(base_url)
except requests.exceptions.RequestException as e:
    print(f'Error : {e}')
except requests.exceptions.JSONDecodeError as error:
    print(f'Error : {error}')
else:
    if requests.status_codes != requests.codes.ok:
        print('There is no information with the data you provided')
    else:
        with open(f'{location}.json', 'w') as f:
            json.dump(response.json(), f)
