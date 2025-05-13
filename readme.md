# Запуск проекта
1) Установить все зависимости проекта:
    ```commandline
    pip install -r requirements.txt
    ```
2) Создать .env файл по примеру из .env.example:
   ```
    POSTGRES_HOST=localhost
    POSTGRES_PORT=5432
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=pswd
    POSTGRES_DB=db_name
    ```
3) Прогнать миграции alembic:
    ```commandline
   alembic upgrade head
    ```
4) Запустить проект из модуля main.py