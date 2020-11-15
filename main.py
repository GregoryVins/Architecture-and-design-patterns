from logging_mode import Logger, debug
from models import TrainingSite
from source.Application import MockApplication
from source.templates import render

SITE = TrainingSite()
LOGGER = Logger('main')


def main_view(request):
    LOGGER.log('Список курсов')
    return '200 OK', render('course_list.html', objects_list=SITE.courses)


@debug
def create_course(request):
    if request['method'] == 'POST':
        data = request['data']
        name = data['name']
        category_id = data.get('category_id')
        print(f'{category_id=}')
        category = None
        if category_id:
            category = SITE.find_category_by_id(int(category_id))
            course = SITE.create_course('record', name, category)
            SITE.courses.append(course)
        return '200 OK', render('create_course.html')
    else:
        categories = SITE.categories
        return '200 OK', render('create_course.html', categories=categories)


def create_category(request):
    if request['method'] == 'POST':
        data = request['data']
        name = data['name']
        category_id = data.get('category_id')

        category = None
        if category_id:
            category = SITE.find_category_by_id(int(category_id))
        new_category = SITE.create_category(name, category)
        SITE.categories.append(new_category)
        return '200 OK', render('create_category.html')
    else:
        categories = SITE.categories
        return '200 OK', render('create_category.html', categories=categories)


urlpatterns = {
    '/': main_view,
    '/create-course/': create_course,
    '/create-category/': create_category,
}


def secret_controller(request):
    request['secret'] = 'secret'


front_controllers = [
    secret_controller,
]

application = MockApplication(urlpatterns, front_controllers)


@application.add_route('/copy-course/')
def copy_course(request):
    request_params = request['request_params']
    print(request_params)
    name = request_params['name']
    old_course = SITE.get_course(name=name)
    if old_course:
        new_name = f'copy_{name}'
        new_course = old_course.clone()
        new_course.name = new_name
        SITE.courses.append(new_course)
    return '200 OK', render('course_list.html', objects_list=SITE.courses)


@application.add_route('/category-list/')
def category_list(request):
    LOGGER.log('Список категорий')
    return '200 OK', render('category_list.html', objects_list=SITE.categories)
