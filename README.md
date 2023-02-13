Innotter - аналог твиттера со своими плюшками.

[Микросервис](https://github.com/Sheshkon/innotter_stats) для мониторинга статистики

Нефункциональные требования:

- Общее:
  - UNIX подобная система (Ubuntu предпочтителен)
  - Работа по GitHub Flow
    - две основных ветки (master, dev)
    - ответвляемся всегда от dev в feature-ветки
    - делаем работу в них и пушим
    - делаем pull request в dev
    - когда сделали pull request, пишем ментору, приступаем к новой задаче не дожидаясь ревью
    - если ментор оставит комментарии на pr, исправляем и заливаем изменения
    - если ментор аппрувит pr то заливаем его в dev
  - PostgreSQL в качестве бд для core app
  - AWS DynamoDB для микросервиса
  - Для хранения файлов использовать AWS S3
  - Для отправки email использовать AWS SES
  - Две разные очереди RabbitMQ для микросервиса и Celery
- Python:
  - Common:
- Последняя стабильная версия
- Для управления виртуальным окружением использовать [pipenv](https://pypi.org/project/pipenv/) **или** [poetry](https://pypi.org/project/poetry/)
- Следовать [PEP 8](https://www.python.org/dev/peps/pep-0008/) ([русская версия](https://pythonworld.ru/osnovy/pep-8-rukovodstvo-po-napisaniyu-koda-na-python.html))
- Связь между микросервисом и основной аппкой через RabbitMQ
- Для взаимодействия с AWS использовать [boto3](https://pypi.org/project/boto3/)
- Валидация JWT-токена в обоих приложениях
- Вся бизнес-логика должна быть покрыта юнит тестами, использовать оба подхода (mock, fixture)
- Core app:
  - Django + [Django Rest Framework](https://www.django-rest-framework.org/)
  - Использовать ViewSets + routers
  - Использовать ModelSerializer
  - Celery + RabbitMQ для отправки уведомлений
  - Отделять бизнес-логику приложения от views в отдельные сервисы.
  - Кастомная JWT аутентификация с помощью Middleware (разрешается использовать [PyJWT](https://pypi.org/project/PyJWT/))
- Microservice:
- FastAPI
- Pydantic
- Readme файл с описанием структуры проекта и команд
- Docker + docker-compose:
- Точка входа выносится в отдельный файл (entrypoint.sh)
- Один Dockerfile на Celery и Django, но разные входные точки
- Отдельный Dockerfile для микросервиса
- База данных должна быть развернута в docker-compose

Функциональные требования:

У пользователя может быть одна из 3 ролей:

- Администратор
- Модератор
- Юзер
1) Администратор имеет права просматривать любые страницы, блокировать их на любой промежуток времени и перманентно, удалять любые посты и блокировать пользователей. Также администратор имеет доступ к админ панели.
1) Модератор имеет права просматривать любые страницы, блокировать их на любой промежуток времени, удалять любые посты.
1) Пользователь может:
1) зарегистрироваться, залогиниться
1) создать страницу, редактировать ее название, uuid и описание, добавлять и удалять к ней теги, делать ее приватной/публичной
1) подписываться на чужие страницы (кидать запрос на подписку в случае приватных страниц)
1) смотреть список желающих подписаться на страницу (в случае приватной) и подтверждать/отказывать в подписке (по одному или сразу всем)
1) писать посты на своих страницах, редактировать их, удалять
1) лайкать/анлайкать посты, отвечать на них от лица какой-либо из собственных страниц
7) просмотреть пролайканные посты
4) Аватары пользователей и страниц хранятся в облачном хранилище.

Система должна:

1) Отправлять уведомления подписчикам на email о новых постах.
1) Показывать новостную ленту (все новые посты подписанных и своих страниц)
1) Автоматически блокировать все страницы пользователя, если пользователь заблокирован
1) Предоставлять поиск страниц по названию/uuid/тегу и пользователей по username/имени (c помощью одного эндпоинта)
1) Делать проверку расширений загружаемых файлов
1) Показывать статистику страниц (количество постов, подписчиков, лайков и т.д.), которая формируется на [микросервисе](https://github.com/Sheshkon/innotter_stats), только пользователям-владельцам страниц

Последовательность действий

1) Создать приватный гит репозиторий и дать доступ своему ментору.
1) Создать AWS аккаунт (в связи с тем что доступ может появится через неделю)
   1) Если aws не присылает код подтверждение можно использовать sms receiver online
   1) После конца тестового задания удалите все сервисы на авс, для избежания списывания денег
1) Создание проекта + настройка окружения
   1) Создание django проекта
   1) Установка всех нужных пакетов через poetry или pipenv
   1) вынос всей sensitive data в .env с помощью python-dotenv
1) Docker + docker-compose
1) Модели
1) CRUD + logic + permissions
1) Celery + AWS
1) Microservice