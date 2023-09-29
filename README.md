![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white) ![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)


# Проект YaMDb 

YaMDb собирает отзывы пользователей на произведения. Произведения делятся на категории: «Книги», «Фильмы», «Музыка».
Пользователи могут оставить один отзыв для одного произведения. Также они могут оставлять комментарии под другими отзывами.

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Aleksentcev/api_yamdb.git
```

```
cd api_final_yatube
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```
```
source venv/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Импортировать данные из csv файлов:

```
python3 manage.py import_csv
```

Запустить проект:

```
python3 manage.py runserver
```

### Панель администратора:

Создать суперпользователя:

```
python3 manage.py createsuperuser
```

Придумать и ввести имя пользователя:

```
Имя пользователя: <username>
```

Ввести адрес электронной почты:

```
Адрес эл.почты: <email>
```

Придумать и ввести пароль (поле ввода не будет отображать никакие символы):

```
Password: <password>
```

Повторно ввести пароль (поле ввода не будет отображать никакие символы):

```
Password (again): <password>
```

URL панели-администратора:

```
.../admin/
```

В панели администратора есть возможность просматривать и редактировать данные из базы данных.


### API:

URL подробной документации к API:

```
.../redoc/
```

### Примеры запросов к API:

Запрос:

```
GET .../api/v1/categories/
```

Ответ:

```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "name": "string",
      "slug": "string"
    }
  ]
}
```

Запрос:

```
POST .../api/v1/titles/10/reviews/

{
  "text": "string",
  "score": 5
}
```

Ответ:

```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 5,
  "pub_date": "2022-08-24T14:15:22Z"
}
```

Запрос:

```
PATCH .../api/v1/titles/2/

{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```

Ответ:

```
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "string"
    }
  ],
  "category": {
    "name": "string",
    "slug": "string"
  }
}
```


### Стек технолгий, использованный в проекте:

```
requests==2.26.0
Django==3.2
djangorestframework==3.12.4
django-filter==23.1
djangorestframework-simplejwt==4.8.0
PyJWT==2.1.0
pytest==6.2.4
pytest-django==4.4.0
pytest-pythonpath==0.7.3
```

### Над проектом работали:

Александр	Иващенко - Модели/View/Эндпойнты,
Дмитрий Кателевский - Отзывы/Комментарии/Рейтинг,
Михаил Алексенцев (тимлид) - Управление пользователями

[![Telegram](https://img.shields.io/badge/aleksentcev-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white&link=https://t.me/aleksentcev)](https://t.me/aleksentcev)
