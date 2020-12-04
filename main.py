from logging_mode import Logger, debug
from mappers import MapperRegistry
from models import TrainingSite, BaseSerializer
from source.Application import Application
from source.CBV import ListView, CreateView
from source.templates import render
from sourceorm.unitofwork import UnitOfWork

SITE = TrainingSite()
LOGGER = Logger('main')

UnitOfWork.new_current()
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)


def main_view(request):
    LOGGER.log('Список курсов')
    return '200 OK', render('course_list.html', objects_list=SITE.courses)


@debug
def create_course(request):
    if request['method'] == 'POST':
        data = request['data']
        name = data['name']
        category_id = data.get('category_id')
        if category_id:
            category = SITE.find_category_by_id(int(category_id))
            course = SITE.create_course('record', name, category)
            SITE.courses.append(course)
        categories = SITE.categories
        return '200 OK', render('create_course.html', categories=categories)
    else:
        categories = SITE.categories
        return '200 OK', render('create_course.html', categories=categories)


class CreateCategoryViewSet(CreateView):
    template_name = 'create_category.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['categories'] = SITE.categories
        return context

    def create_obj(self, data: dict):
        name = data['name']
        category_id = data.get('category_id')

        category = None
        if category_id:
            category = SITE.find_category_by_id(int(category_id))

        new_category = SITE.create_category(name, category)
        SITE.categories.append(new_category)


class CategoryListViewSet(ListView):
    queryset = SITE.categories
    template_name = 'category_list.html'


class StudentListViewSet(ListView):
    queryset = SITE.students
    template_name = 'student_list.html'

    def get_queryset(self):
        mapper = MapperRegistry.get_current_mapper('student')
        return mapper.all()


class StudentCreateViewSet(CreateView):
    template_name = 'create_student.html'

    def create_obj(self, data: dict):
        name = data['name']
        new_obj = SITE.create_user('student', name)
        SITE.students.append(new_obj)
        new_obj.mark_new()
        UnitOfWork.get_current().commit()


class AddStudentByCourseCreateViewSet(CreateView):
    template_name = 'add_student.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['courses'] = SITE.courses
        context['students'] = SITE.students
        return context

    def create_obj(self, data: dict):
        course_name = data['course_name']
        course = SITE.get_course(course_name)
        student_name = data['student_name']
        student = SITE.get_student(student_name)
        course.add_student(student)


urlpatterns = {
    '/': main_view,
    '/create-course/': create_course,
    '/create-category/': CreateCategoryViewSet(),
    '/category-list/': CategoryListViewSet(),
    '/student-list/': StudentListViewSet(),
    '/create-student/': StudentCreateViewSet(),
    '/add-student/': AddStudentByCourseCreateViewSet(),
}


def secret_controller(request):
    request['secret'] = 'secret'


front_controllers = [
    secret_controller,
]

application = Application(urlpatterns, front_controllers)


@application.add_route('/copy-course/')
def copy_course(request):
    request_params = request['request_params']
    name = request_params['name']
    old_course = SITE.get_course(name=name)
    if old_course:
        new_name = f'copy_{name}'
        new_course = old_course.clone()
        new_course.name = new_name
        SITE.courses.append(new_course)
    return '200 OK', render('course_list.html', objects_list=SITE.courses)


@application.add_route('/api/')
def course_api(request):
    return '200 OK', BaseSerializer(SITE.courses).save()
