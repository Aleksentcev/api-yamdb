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

### Над проектом работали:

Александр	Иващенко - Модели/View/Эндпойнты,
Дмитрий Кателевский - Отзывы/Комментарии/Рейтинг,
Михаил Алексенцев - Управление пользователями.
