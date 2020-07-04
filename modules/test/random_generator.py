from random import choice
from random import random
from random import randint

from os import path
from os import getcwd
from os import makedirs

import string
from datetime import datetime, timedelta

class RandomGenerator:

    def generate_string(self, min_length, max_length):
        farsi_letters = 'ابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی'
        random_length = randint(min_length, max_length)
        list_of_choices = farsi_letters + string.ascii_letters + string.digits
        random_chars = [choice(list_of_choices) 
                            for i in range(random_length)]
        return ''.join(random_chars)

    def generate_bool(self):
        return choice([True, False])

    def generate_real(self, min, max):
        return random() * (max - min) + min

    def generate_int(self, min, max):
        return randint(min, max)

    # generate a datetime in format yyyy-mm-dd hh:mm:ss.000000
    def generate_date_time(
            self, min_year = 1900, max_year = datetime.now().year):
        start = datetime(min_year, 1, 1, 00, 00, 00)
        years = max_year - min_year + 1
        end = start + timedelta(days = 365 * years)
        return start + (end - start) * random()

    def generate_path(self, level, base = ""):
        _path = base
        for i in range(level):
            sub_path = self.generate_string(1, 5)
            _path = path.join(_path, sub_path)
        return _path

    def generate_file(self, _path):
        with open(_path, 'w') as _file:
            _file.write(self.generate_string(1000, 1000000))

    def generate_dirs(self, base, level):
        _path = self.generate_path(level, base)
        makedirs(_path)
        return _path