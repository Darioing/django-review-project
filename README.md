# django-review-project
Дипломная работа с сайтом Django для учета рейтингов ресторанов в моём(пока что) городе

source venv/Script/activate

## Миграции
1. python manage.py makemigrations users
2. python manage.py makemigrations reviews
3. python manage.py makemigrations
4. python manage.py migrate

## Запуск React
1. Нужен Node.js
2. cd front_end
3. npm start

## Запуск Django
1. python manage.py runserver

## Создание бд из копии
1. python manage.py loaddata db_dump.json
