from random import randint

from .view import index_view, contacts_view
from .source.Application import Application

urlpatterns = {
    '/': index_view,
    '/contacts/': contacts_view,
}


def secret_key(request):
    request['key'] = 'secret key'


def random_num(request):
    request['number'] = str(randint(0, 100))


front_controllers = [
    secret_key,
    random_num,
]

application = Application(urlpatterns, front_controllers)
