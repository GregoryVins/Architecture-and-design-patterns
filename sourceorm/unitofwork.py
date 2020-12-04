import threading


class UnitOfWork:
    """Паттерн Unit of Work."""

    current = threading.local()

    def __init__(self):
        self.new_objects = []
        self.old_objects = []
        self.deleted_objects = []

    def set_mapper_registry(self, MapperRegistry):
        self.MapperRegistry = MapperRegistry

    def register_new(self, obj):
        self.new_objects.append(obj)

    def register_old(self, obj):
        self.old_objects.append(obj)

    def register_deleted(self, obj):
        self.deleted_objects.append(obj)

    def commit(self):
        self.insert_new()
        self.update_old()
        self.remove_deleted()

    def insert_new(self):
        for item in self.new_objects:
            self.MapperRegistry.get_mapper(item).insert(item)

    def update_old(self):
        for item in self.old_objects:
            self.MapperRegistry.get_mapper(item).update(item)

    def remove_deleted(self):
        for item in self.deleted_objects:
            self.MapperRegistry.get_mapper(item).delete(item)

    @staticmethod
    def new_current():
        __class__.set_current(UnitOfWork())

    @classmethod
    def set_current(cls, unit_of_work):
        cls.current.unit_of_work = unit_of_work

    @classmethod
    def get_current(cls):
        return cls.current.unit_of_work


class DomainObject:

    def mark_new(self):
        UnitOfWork.get_current().register_new(self)

    def mark_old(self):
        UnitOfWork.get_current().register_old(self)

    def mark_deleted(self):
        UnitOfWork.get_current().register_deleted(self)