# Fastapi_project

## Запуск

1. Клонировать репозиторий
   
    git clone <ссылка с git-hub>
   
2. Перейти в папку /YLAB

3. Активать окружение
   
   source venv/bin/activate

4. Создать БД. В моем примере - "YlabHW1" в PostgreSQL

6. Требуется прописать файл .env с данными БД - пример в репозитории.

7. Прогнать скрипт очистки БД

   python clearDB.py

8. Прогнать миграции

   alembic upgrade head

9. Запустить сервер

   uvicorn src.main:app --reload

10. Документация доступна по адресу <http://127.0.0.1:8000/docs>

Для build: docker compose build
Для поднятия: docker compose up



HW2:

1. Для build тестов: docker-compose -f docker-compose.test.yml build

1. Поднимаем docker в фоновом режиме: docker-compose -f docker-compose.test.yml up -d

2. Входим в консоль: docker exec -it fastapi_app /bin/bash

3. Прогоняем тесты:
pytest -v -s tests/test_menu.py
pytest -v -s tests/test_submenu.py
pytest -v -s tests/test_dish.py
pytest -v -s tests/test_count.py

4. Документация доступна по адресу: http://localhost:9999/docs

5. В src/scripts/query.py лежит запрос для вывода количества подменю и блюд для меню.