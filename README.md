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

## Docker
1. docker builder prune --all / чисто для галочки удаляем все контейнеры, а то вдруг что
2. docker-compose down --volumes / остановка всех контейнеров
3. docker-compose up --build -d / билдим контейнеры из Dockerfile и запускаем их в фоне
4. docker exec -it _django-backend_ bash / Для перехода в конкретный контейнер заменяем django-backend на имя контейнера
5. python manage.py loaddata data.json / Загрузка данных
6. docker-compose build _frontend_ / пересборка конкретного контейнера, заменяем frontend на контейнер
7. docker-compose up -d _frontend_ / Перезапуск конкретного контейнера, заменяем frontend на контейнер



