# Архитектура и шаблоны проектирования на Python
*4 четверть курса Python разработки от университета GeekBrains*

[![GregoryVins](img/pwd.jpg)](https://github.com/GregoryVins/Architecture-and-design-patterns)


### Урок 1
- Начало разработки своего WSGI framework
- Использование классических паттернов page controller и front controller (Возможность отвечать на get запросы пользователя)
- Рендеринг страниц с помощью шаблонизатора jinja2
- Добавление двух демонстрационных html страниц (index, contacts)

### Установка и запуск

**Установка зависимостей:**
```
$ pip install uwsgi
$ pip install jinja2
```
**Запуск:**

Переходим в папку lesson 1 (cd "/..path../lesson 1"), где расположен файл main.py
```
$ uwsgi --http :8000 --wsgi-file main.py
```