class Application:
    """
    Создаем класс, чтобы пробросить в него данные без нарушения PEP3333.
    """

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
        if path in self.routes:
            view = self.routes[path]

            request = {}
            for front_controller in self.f_controllers:
                front_controller(request)

            code, body = view(request)
            start_response(code, [('Context-Type', 'text/html')])
            return [body.encode('UTF-8')]

        view = self.routes['/error/']
        request = {}
        code, body = view(request)
        start_response(code, [('Context-Type', 'text/html')])
        return [body.encode['UTF-8']]
