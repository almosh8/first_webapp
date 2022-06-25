FROM python:3.10-slim

RUN mkdir /app

COPY requirements.txt /app

RUN pip3 install -r /app/requirements.txt --no-cache-dir

COPY ./ /app

WORKDIR /app

# Выполнить запуск сервера разработки при старте контейнера.
CMD ["python", "manage.py", "runserver" ]