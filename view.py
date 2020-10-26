from datetime import datetime

from source.templates import render


def index_view(request):
    data = request['key']
    return '200 OK', render('index.html', data=data)


def contacts_view(request):
    if request['method'] == 'POST':
        print('\n\n', request)
        data = request['data']
        topic = data['topic']
        email = data['email']
        message = data['message']

        save_temporary_data(email=email, topic=topic, message=message)
        return '200 OK', render('contacts.html')
    return '200 OK', render('contacts.html')


def not_found_404(request):
    return '404 NOT FOUND', render('404_not_found.html')


def save_temporary_data(email, topic, message):
    """
    :param email: User's email address .
    :param topic: User's title or theme of message.
    :param message: User's text message.
    """
    with open('temp/temporary.txt', 'a')as file:
        file.write(f'{datetime.now()} / from user: {email}.\n'
                   f'Topic: {topic} / Text: {message}\n\n')
