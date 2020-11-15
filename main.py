from hashlib import sha256
from random import randint

from source.Application import Application
from source.templates import render

from view import index_view, contacts_view, not_found_404

urlpatterns = {
    '/': index_view,
    '/contacts/': contacts_view,
    '/error/': not_found_404,
}


def secret_key(request):
    request['key'] = sha256(bytes(randint(0, 100))).hexdigest()


front_controllers = [
    secret_key,
]

application = Application(urlpatterns, front_controllers)
