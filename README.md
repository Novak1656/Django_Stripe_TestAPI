# Django + Stripe API
Тестовое задание от компании Ришат

## Задание
https://docs.google.com/document/d/1RqJhk-pRDuAk4pH1uqbY9-8uwAqEXB9eRQWLSMM_9sI/edit#heading=h.mcl6i4g8bfll

Выполненные бонусные задания:
1. Запуск используя Docker
2. Использование environment variables
3. Просмотр Django Моделей в Django Admin панели
4. Модель Order, в которой можно объединить несколько Item и сделать платёж в Stripe на содержимое Order c общей стоимостью всех Items
5. Модели Discount, Tax, которые можно прикрепить к модели Order и связать с соответствующими атрибутами при создании платежа в Stripe - в таком случае они корректно отображаются в Stripe Checkout форме. 

## Руководство по запуску

1. Необходимо создать и активировать виртуальное окружение.
2. Скопируйте репозиторий git
```
git clone https://github.com/Novak1656/Django_Stripe_TestAPI.git
```   
3. В корневой директории, где распологается файл .gitignore и docker-compose.yml создайте файл '.env'.
Содержание файла должно быть следущим:
```
SECRET_KEY='Секретный ключ Django'

STRIPE_PUBLIC_KEY='Публичный ключ от Stripe API'
STRIPE_SECRET_KEY='Секретный ключ от Stripe API'

POSTGRES_USER='Имя пользователя от Postgresql'
POSTGRES_PASSWORD='Пароль от Postgresql'
POSTGRES_DB='Название базы данных'
POSTGRES_HOST='Хост базы данных'
POSTGRES_PORT='Порт базы данных'

DJANGO_SUPERUSER_USERNAME='Имя для администатора'
DJANGO_SUPERUSER_EMAIL='Email для администатора (не обязательно)'
DJANGO_SUPERUSER_PASSWORD='Пароль для администатора'
```
4. Запуск приложения
Для запуска используя Docker находясь в дирректории проекта выполните следующие команды в терминале 
```
cd university
docker-compose up -d --build
```
Для обычного запуска выполните следующие команды в терминале
```
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py initadmin
python manage.py createitems 'Кол-во создаваемых записей в бд'
python manage.py creatediscounts 'Кол-во создаваемых записей в бд'
python manage.py createtax 'Кол-во создаваемых записей в бд'
python manage.py createorders 'Кол-во создаваемых записей в бд'
python manage.py runserver
```
5. Перейдите по любому из маршрутов api

## Маршруты API
### Основные
```
http://127.0.0.1:8000/buy/<int:pk> - Получить id сессии stripe при покупке предмета
http://127.0.0.1:8000/item/<int:pk> - Страница предмета
```

### Бонусные
```
http://127.0.0.1:8000/admin/ - Панель администратора
http://127.0.0.1:8000/order/<int:order_pk> - Страница заказа
http://127.0.0.1:8000/order/<int:order_pk>/buy/ - Получить id сессии stripe при покупке заказа
```
