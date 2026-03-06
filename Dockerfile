FROM python:3.11-slim

WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование всего проекта
COPY . .

# Создание папки для базы данных (том будет смонтирован сюда)
RUN mkdir -p /app/data

# Указываем переменную окружения для пути к БД
ENV DB_PATH=/app/data/japanese_bot.db

# Открываем порт для API (как в bot.py)
EXPOSE 8080

# Запуск бота
CMD ["python", "bot.py"]
