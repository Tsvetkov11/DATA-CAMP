# Крок 1: Беремо легковаговий базовий образ Python
FROM python:3.10-slim

# Крок 2: Створюємо робочу папку в контейнері
WORKDIR /app

# Крок 3: Копіюємо requirements.txt та встановлюємо ліби (використовуємо кеш)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Крок 4: Копіюємо всі наші файли (код, скріншоти, README) у контейнер
COPY . .

# Крок 5: Інформуємо Docker, що додаток працює на 8000 порту
EXPOSE 8000

# Крок 6: Гнучке налаштування згідно з Критерієм №2 (ENTRYPOINT + CMD)
ENTRYPOINT ["python"]
CMD ["-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]