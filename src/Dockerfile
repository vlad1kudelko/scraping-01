FROM python:3

RUN apt update && apt install -y chromium

# установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# настройка прав
RUN useradd -m user
USER user
WORKDIR /home/user

COPY main.py .
