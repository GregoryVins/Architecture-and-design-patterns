from jinja2 import FileSystemLoader
from jinja2.environment import Environment


def render(template_name, folder='templates', **kwargs):
    """
    Отвечает за рендер страницы
    :param template_name: Название шаблона
    :param folder: Название папки, где расположены шаблоны
    :return: Рендерит шаблон с передаваемыми аргументами
    """
    environment = Environment()
    environment.loader = FileSystemLoader(folder)
    template = environment.get_template(template_name)
    return template.render(**kwargs)
