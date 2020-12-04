import pickle

from reuserpatterns.observer import Subject
from reuserpatterns.prototype import PrototypeMixin
from sourceorm.unitofwork import DomainObject


class User:
    """Базовая модель пользователя."""

    def __init__(self, name):
        self.name = name


class Teacher(User):
    """Модель преподавателя."""

    def __init__(self, name):
        super().__init__(name)
        self.subject = []


class Student(User, DomainObject):
    """Модель студента."""

    def __init__(self, name):
        super().__init__(name)
        self.courses = []


# class SimpleFactory:
#     """Абстрактный паттерн фабричного метода."""
#
#     def __init__(self, types=None):
#         self.types = types or {}


class UserFactory:
    types = {
        'student': Student,
        'teacher': Teacher,
    }

    @classmethod
    def create(cls, type_, name):
        return cls.types[type_](name)


class Category:
    """Модель категории с автоинкрементом поля ID."""
    id = 0

    def __getitem__(self, item):
        return self.courses[item]

    def __init__(self, name, category):
        self.id = Category.id
        Category.id += 1
        self.name = name
        self.category = category
        self.courses = []

    def course_count(self):
        """Возвращает количество курсов."""
        result = len(self.courses)
        if self.category:
            result += self.category.course_count()
        return result


class Course(PrototypeMixin, Subject):
    """Модель курса."""

    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)
        self.students = []
        super().__init__()

    def __getitem__(self, item):
        return self.students[item]

    def add_new_student(self, student: Student):
        self.students.append(student)
        student.courses.append(self)


class BaseSerializer:

    def __init__(self, objct):
        self.objct = objct

    def save(self):
        return pickle.dumps(self.objct)

    def load(self, objct):
        return pickle.loads(objct)


class InteractiveCourse(Course):
    """Модель интерактивных курсов (вебиныр)."""


class RecordCourse(Course):
    """Модель курсов, которые были записаны."""


class CourseFactory:
    types = {
        'interactive': InteractiveCourse,
        'record': RecordCourse
    }

    @classmethod
    def create(cls, type_, name, category):
        return cls.types[type_](name, category)


class TrainingSite:
    """Основная модель сайта."""

    def __init__(self):
        self.teachers = []
        self.students = []
        self.courses = []
        self.categories = []

    def create_user(self, type_, name):
        """СОздание пользователя в зависимости от типа."""
        return UserFactory.create(type_, name)

    def create_category(self, name, category=None):
        """Создание категории."""
        return Category(name, category)

    def find_category_by_id(self, id):
        """
        Поиск категории по ID.
        Возвращает ошибку в случае отсутствия.
        """
        for item in self.categories:
            print(f'{item.id=}')
            if item.id == id:
                return item
        raise Exception(f'Категории с {id} не существует')

    def create_course(self, type_, name, category):
        """Создание курса."""
        return CourseFactory.create(type_, name, category)

    def get_course(self, name):
        """
        Получение курса по имени.
        Возвращает None, если курс не найден.
        """
        for item in self.courses:
            if item.name == name:
                return item

    def get_student(self, name):
        for item in self.students:
            if item.name == name:
                return item
