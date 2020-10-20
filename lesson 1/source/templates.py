import os
from jinja2 import Template


def render(template_name, folder='templates', **kwargs):
    """
    Минимальная функциональность шаблонизатора.
    :param folder: Имя папки, где находится шаблон.
    :param template_name: Имя шаблона.
    :param kwargs: Параметры для передачи.
    """
    path = os.path.join(folder, template_name)
    with open(path, encoding='UTF-8')as file:
        template = Template(file.read())
    return template.render(**kwargs)
