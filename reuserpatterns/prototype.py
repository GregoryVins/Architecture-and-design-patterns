import copy


class PrototypeMixin:
    """
    Классическая реализация паттерна
    """

    def clone(self):
        return copy.deepcopy(self)
