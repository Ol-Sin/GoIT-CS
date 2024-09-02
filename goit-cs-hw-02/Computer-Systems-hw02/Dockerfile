# Використовуємо офіційний образ Python як базовий
FROM python:3.12.2

# Встановлюємо робочу директорію в контейнері
WORKDIR /app

# Копіюємо файл requirements.txt у контейнер
COPY requirements.txt .

# Встановлюємо залежності
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо весь проект у контейнер
COPY . .

# Відкриваємо порт для застосунку
EXPOSE 8000

# Команда для запуску FastAPI застосунку
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
