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
        self.parser.add_argument('-s', '--start', type=validate_date,
                                 help='Initial date to get weather data shema: YYYY-MM-DD')
        self.parser.add_argument('-e', '--end', type=validate_date,
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
            status = response.status_code // 100
            if status == 4:
                print('Client error')
            elif status == 5:
                print('Server error')
            else:
                self.save(response.json())

    def run(self):
        self.args = self.parser.parse_args()
        if self.args.location or self.args.latitude:
            self.base_url = f'{self.base_url}{self.args.location or self.args.latitude}'
            if self.args.start and self.args.end:
                if self.args.start < self.args.end:
                    print(f'Start date: {self.args.start} should be smaller than End date: {self.args.end}')
                    return
            if self.args.start:
                self.base_url = f'{self.base_url}/{self.args.start}'
            if self.args.end:
                self.base_url = f'{self.base_url}/{self.args.end}'
            self.base_url = f'{self.base_url}?key={self.key}'
            self.request()
        else:
            print('Either location or latitude must be provided')


def validate_location(value):
    if ',' not in value:
        raise argparse.ArgumentTypeError(f'The entry you provided is not in right format: {value}, Shema : London,UK')
    elif len(value.split(',')) != 2:
        raise argparse.ArgumentTypeError('You can provide one location at a time')
    return value


def validate_latitude(value):
    if ',' not in value:
        raise argparse.ArgumentTypeError('The entry you provided is not in right format: {value}, Shema : '
                                         'numbers:numbers')
    elif len(value.split(',')) != 2:
        raise argparse.ArgumentTypeError('You can provide one location at a time')
    elif not all([i.isnumeric() for i in value.split(',')]):
        raise argparse.ArgumentTypeError(
            f'The value you provided should be both numbers, values: {value}')
    return value


def validate_date(value):
    formats = ['%Y-%m-%d', '%Y-%m-%dT%H:%M:%S']
    for format_ in formats:
        try:
            return datetime.datetime.strptime(value, format_).date()
        except ValueError:
            continue

    try:
        timestamp = int(value)
        return datetime.datetime.fromtimestamp(timestamp)
    except (ValueError, OverflowError):
        raise argparse.ArgumentTypeError(
            f'Invalid date format: {value}\n'
            f'Valid formats are {" or ".join(formats)} or Unix timestamp'
        )


if __name__ == '__main__':
    app = WeatherAPI()
    app.run()
