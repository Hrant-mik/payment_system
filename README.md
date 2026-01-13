# Payment System с Stripe

## Описание

Django-приложение для демонстрации интеграции с платежной системой Stripe.

## Локальный запуск без Docker

1. Клонировать репозиторий:
```bash
git clone https://github.com/Hrant-mik/payment_system
cd payment_system
```
2. Создать виртуальное окружение:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```
3. Установить зависимости:
```bash
pip install -r requirements.txt
```
4. Создать `.env` с переменными:
```
DJANGO_SECRET_KEY=supersecret
STRIPE_PUBLIC_KEY=pk_test_xxxxxxxxxxxxx
STRIPE_SECRET_KEY=sk_test_xxxxxxxxxxxxx
DEBUG=True
```
5. Применить миграции и создать суперпользователя:
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser --username admin --email admin@example.com
# Пароль: admin123
```
6. Запустить сервер:
```bash
python manage.py runserver
```

Сервер будет доступен: [http://localhost:8000](http://localhost:8000)

## Запуск с Docker

1. Клонировать репозиторий:
```bash
git clone https://github.com/Hrant-mik/payment_system
cd payment_system
```
2.  Собрать и запустить контейнеры:
```bash
docker compose up --build
```
2. Сервер и админ панель:
- [http://localhost:8000](http://localhost:8000)
- Админ: `admin` / `admin123`
- Все миграции и создание админа выполняются автоматически через start.sh.
