# Dockerfile для Flask-сервера
FROM python:3.12

WORKDIR /app

# Встановлення залежностей
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

# Запуск Flask-сервера
CMD ["python", "main.py"]
