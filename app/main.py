import argparse
import json

import requests

from local_settings import API_KEY


class WeatherAPI:
    def __init__(self):
        self.base_url = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/'
        self.key = API_KEY
        self.parser = argparse.ArgumentParser(prog='Weather API')
        self.add_argument()

    def add_argument(self):
        self.parser.add_argument('-l', '--location', required=True, type=validate_comma,
                                 help='location attribute for weather data\nshema: {\nLondon,Uk\n}')
        self.parser.add_argument('-d1', '--date1', type=str, help='Initial date to get weather data')
        self.parser.add_argument('-d2', '--date2', type=str, help='Final date to get weather data')

    def save(self, data):
        with open(f'{self.args.location}.json', 'w') as f:
            json.dump(data, f)

    def request(self):
        try:
            response = requests.get(self.base_url)
        except requests.exceptions.RequestException as e:
            print(f'Error : {e}')
        else:
            if response.status_code != requests.codes.ok:
                print('There is no information with the data you provided')
            else:
                self.save(response.json())

    def run(self):
        self.args = self.parser.parse_args()
        self.base_url = f'{self.base_url}{self.args.location}?key={self.key}'
        self.request()


def validate_comma(value):
    if ',' not in value:
        raise argparse.ArgumentTypeError('The location you entered is incorrect')
    return value


if __name__ == '__main__':
    app = WeatherAPI()
    app.run()
