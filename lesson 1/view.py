from source.templates import render


def index_view(request):
    data = request['key']
    return '200 OK', render('index.html', data=data)


def contacts_view(request):
    data = request['number']
    return '200 OK', render('contacts.html', data=data)


def not_found_404(request):
    return '404 NOT FOUND', render('404_not_found.html')
