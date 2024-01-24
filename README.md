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
