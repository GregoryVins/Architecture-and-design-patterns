from reuserpatterns.singletones import SingletonByName
from time import time


class Logger(metaclass=SingletonByName):

    def __init__(self, name):
        self.name = name

    def log(self, text):
        print(f'Log --> {text}')


def debug(foo):
    def inner(*args, **kwargs):
        start = time()
        result = foo(*args, **kwargs)
        end = time()
        print(f'DEBUG --> {foo.__name__}, {end - start}')
        return result

    return inner


class ConsoleWriter:

    def write(self, text):
        print(text)


class FileWriter:

    def __init__(self, file_name):
        self.file_name = file_name

    def write(self, text):
        with open(self.file_name, 'a', encoding='utf-8') as f:
            f.write(f'{text}\n')
