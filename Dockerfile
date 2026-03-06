FROM python:3.11-slim

WORKDIR /app

# Устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Создаём папку для базы данных (будет смонтирована)
RUN mkdir -p /data

# Указываем порт, который слушает бот (в bot.py у вас 8080)
EXPOSE 8080

# Запускаем бота
CMD ["python", "bot.py"]
