## О проекте:

Данный проект представляет из себя коллекцию тестов для двух веб-приложений (сайты с новостями и заметками пользователя) на pytest и unittest.

## Как запустить проект:

1) Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Leonid-Agalakov-89/django_testing.git
```

```
cd django_testing
```

2) Cоздать и активировать виртуальное окружение:

```
python -m venv env
```

```
source env/bin/activate
```

3) Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

4) Выполнить миграции:

```
python manage.py makemigrations
```

```
python manage.py migrate
```

5) Запустить скрипт для `run_tests.sh` из корневой директории проекта:
```sh
bash run_tests.sh
```

## Технологии:

Backend
* Django
* SQLite

Frontend
* HTML

Tests
* pytest
* unittest

## Об авторе:
Леонид Агалаков - python backend developer.
`https://github.com/Leonid-Agalakov-89`
