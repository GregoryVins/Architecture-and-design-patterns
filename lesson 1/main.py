from random import randint
from hashlib import sha256

from view import index_view, contacts_view, not_found_404
from source.Application import Application

urlpatterns = {
    '/': index_view,
    '/contacts/': contacts_view,
    '/error/': not_found_404,
}


def secret_key(request):
    request['key'] = sha256(bytes(randint(0, 100))).hexdigest()


def random_num(request):
    request['number'] = str(randint(0, 100))


front_controllers = [
    secret_key,
    random_num,
]

application = Application(urlpatterns, front_controllers)
