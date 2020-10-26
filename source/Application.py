class Application:
    """
    Создаем класс, чтобы пробросить в него данные без нарушения PEP3333.
    """

    def parse_input_data(self, data: str) -> dict:
        result = {}
        if data:
            params = data.split('&')

            for item in params:
                key, value = item.split('=')
                result[key] = value
        return result

    def parse_wsgi_input_data(self, data: bytes) -> dict:
        result = {}
        if data:
            data_str_type = data.decode(encoding='UTF-8')
            result = self.parse_input_data(data_str_type)
        return result

    def get_wsgi_input_data(self, environ):
        length_data_content = environ.get('CONTENT_LENGTH')
        length_content = int(length_data_content) if length_data_content else 0
        data = environ['wsgi.input'].read(length_content) if length_content > 0 else b''
        return data

    def __init__(self, routes: dict, f_controllers: list):
        """
        Создаём атрибуты класса, где
        :param routes: словарь, dict - urlpatterns.
        :param f_controllers: список, массив, list - front controllers.
        """
        self.routes = routes
        self.f_controllers = f_controllers

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']

        if not path.endswith('/'):
            path += '/'

        method = environ['REQUEST_METHOD']
        data = self.get_wsgi_input_data(environ=environ)
        data = self.parse_wsgi_input_data(data=data)
        query_string = environ['QUERY_STRING']
        request_params = self.parse_input_data(query_string)

        if path in self.routes:
            view = self.routes[path]

            request = {}

            request['method'] = method
            request['data'] = data
            request['request_params'] = request_params

            for front_controller in self.f_controllers:
                front_controller(request)

            code, body = view(request)
            start_response(code, [('Context-Type', 'text/html')])
            return [body.encode('UTF-8')]

        else:
            view = self.routes['/error/']
            request = {}
            code, body = view(request)
            start_response(code, [('Context-Type', 'text/html')])
            return [body.encode('UTF-8')]