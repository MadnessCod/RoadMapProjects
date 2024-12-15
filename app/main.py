import argparse
import json
import datetime

import requests
import redis

from local_settings import API_KEY


class WeatherAPI:
    def __init__(self, expires=datetime.timedelta(days=15), encoding='utf-8'):
        self.base_url = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/'
        self.key = API_KEY
        self.parser = argparse.ArgumentParser(prog='Weather API')
        self.redis = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        self.expires = expires
        self.encoding = encoding
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

    def __getitem__(self, key):
        record = self.redis.exists(key)
        if record:
            print('getting data from cache')
            return json.dumps(self.redis.get(key))
        return None

    def __setitem__(self, content):
        print('saving data to cache')
        if content:
            name = f"{content['address']}-{datetime.datetime.now().strftime('%Y-%m-%d')}"
            self.redis.setex(name, self.expires, json.dumps(content))
            print('data have saved to cache')
        else:
            print('can\'t save data to cache')

    def request(self):
        try:
            response = requests.get(self.base_url)
        except requests.exceptions.RequestException as e:
            print(f'Error : {e}')
        else:
            status = response.status_code // 100
            if status == 4:
                print(f'Client error: {response.status_code}')
            elif status == 5:
                print(f'Server error: {response.status_code}')
            else:
                self.__setitem__(response.json())

    def decide(self):
        for key in self.redis.scan_iter('*'):
            value = json.loads(self.redis.get(key))
            if self.redis.exists(f'{value["address"]}-{datetime.datetime.now().strftime('%Y-%m-%d')}'):
                data = self.__getitem__(f'{value["address"]}-{datetime.datetime.now().strftime('%Y-%m-%d')}')
                return
        self.request()

    def run(self):
        self.args = self.parser.parse_args()
        if self.args.location or self.args.latitude:
            self.base_url = f'{self.base_url}{self.args.location or self.args.latitude}'
            if self.args.start and self.args.end:
                if self.args.start > self.args.end:
                    print(f'Start date: {self.args.start} should be smaller than End date: {self.args.end}')
                    return
            if self.args.start:
                self.base_url = f'{self.base_url}/{self.args.start}'
            if self.args.end:
                self.base_url = f'{self.base_url}/{self.args.end}'
            self.base_url = f'{self.base_url}?key={self.key}'
            self.decide()
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
