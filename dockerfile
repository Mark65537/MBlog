FROM python:3.12

WORKDIR /app

# системные зависимости
RUN apt-get update && apt-get install -y \
    libpq-dev gcc

# зависимости python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# копируем проект
COPY . .

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

# запуск
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]