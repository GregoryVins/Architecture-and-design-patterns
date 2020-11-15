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
