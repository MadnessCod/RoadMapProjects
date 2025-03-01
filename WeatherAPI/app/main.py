import argparse
import json
import datetime
import sys
import time

import requests
import redis

from local_settings import API_KEY


def rate_limiting(max_calls, period):
    def decorator(func):
        call_times = list()

        def wrapper(*args, **kwargs):
            current_time = time.time()
            while call_times and call_times[0] < current_time - period:
                call_times.pop(0)

                if len(call_times) >= max_calls:
                    sleep_time = period - (current_time - call_times[-1])
                    time.sleep(sleep_time)

                call_times.append(time.time())
            return func(*args, **kwargs)

        return wrapper

    return decorator


class WeatherAPI:
    def __init__(self, redis_client, expires=datetime.timedelta(days=15)):
        self.base_url = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/'
        self.key = API_KEY
        self.parser = argparse.ArgumentParser(prog='Weather API')
        self.redis = redis_client
        self.expires = expires
        self.time_periods = ['today', 'tomorrow', 'yesterday', 'yeartodate', 'monthtodate']
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
        self.parser.add_argument('--i', '--include', type=validate_include,
                                 help='Extra data to request')

    def get(self, key):
        record = self.redis.exists(key)
        if record:
            print('getting data from Redis')
            print(f'Filename is {key}.json')
            return
        return None

    def set(self, content):
        print('saving data to cache')
        if content:
            name = f"{content['address']}-{datetime.datetime.now().strftime('%Y-%m-%d')}"
            self.redis.setex(name, self.expires, json.dumps(content))
            print('data have saved to Redis')
            with open(f'{name}.json', 'w') as f:
                json.dump(json.loads(self.redis.get(name)), f)
            print(f'Data is saved to your system, File name : {name}.json')
        else:
            print('can\'t save data to Redis')

    @rate_limiting(max_calls=10, period=10)
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
                self.set(response.json())

    def decide(self):
        for key in self.redis.scan_iter('*'):
            value = json.loads(self.redis.get(key))
            if self.redis.exists(f'{value["address"]}-{datetime.datetime.now().strftime('%Y-%m-%d')}'):
                self.get(f'{value["address"]}-{datetime.datetime.now().strftime('%Y-%m-%d')}')
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


def validate_include(value):
    elements = ['tempax', 'tempmin', 'temp', 'datetime', 'degreedays']
    if value not in elements:
        raise argparse.ArgumentTypeError(f'the data sould be in right format \nacceptibale formats: {elements}')
    return value


if __name__ == '__main__':
    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    try:
        r.ping()
    except redis.exceptions.ConnectionError:
        print('Redis is not available\n'
              'Check if redis running on localhost, port: 6379\n'
              'for more information visit https://redis.io/docs/latest/develop/get-started/')
        sys.exit()
    app = WeatherAPI(r)
    app.run()
