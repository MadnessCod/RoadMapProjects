import argparse
import json

import requests

import datetime
from local_settings import API_KEY


class WeatherAPI:
    def __init__(self):
        self.base_url = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/'
        self.key = API_KEY
        self.parser = argparse.ArgumentParser(prog='Weather API')
        self.add_argument()

    def add_argument(self):
        self.parser.add_argument('-l', '--location', type=validate_location,
                                 help='location attribute for weather data shema: {London,Uk}')
        self.parser.add_argument('-la', '--latitude', type=validate_latitude,
                                 help='Provide location with longitude and latitude')
        self.parser.add_argument('-d1', '--date1', type=validate_date,
                                 help='Initial date to get weather data shema: YYYY-MM-DD')
        self.parser.add_argument('-d2', '--date2', type=validate_date,
                                 help='Final date to get weather data shema: YYYY-MM-DD')

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
        if self.args.location or self.args.latitude:
            self.base_url = f'{self.base_url}{self.args.location}?key={self.key}'
            self.request()
        else:
            print('Either location or latitude must be provided')


def validate_location(value):
    if ',' not in value:
        raise argparse.ArgumentTypeError('The entry you provided is not a comma-separated')
    return value


def validate_latitude(value):
    if ',' not in value:
        raise argparse.ArgumentTypeError('The entry you provided is not a comma-separated list')
    elif len(value.split(',')) != 2:
        raise argparse.ArgumentTypeError('You can provide one location at a time')
    elif not all([i.isnumeric() for i in value.split(',')]):
        raise argparse.ArgumentTypeError(
            f'The value you provided should be both numbers, values: {[i for i in value.split(',')]}')
    return value


def validate_date(value):
    try:
        return datetime.datetime.strptime(value, '%Y-%m-%d').date()
    except ValueError:
        raise argparse.ArgumentTypeError('The entry you provided is not a valid date')


if __name__ == '__main__':
    app = WeatherAPI()
    app.run()
