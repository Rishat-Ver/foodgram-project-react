# Проект **Foodgram - "Продуктовый помощник"**
![example workflow] Надо добавить!

### **Адрес проекта**
Надо добавить!

---

### **Описание проекта:**
сайт **Foodgram** - «Продуктовый помощник» <br>
На этом сервисе пользователи смогут <br> 
- публиковать рецепты <br>
- подписываться на публикации других пользователей <br>
- добавлять понравившиеся рецепты в список «Избранное»<br>
- скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

---

### **Технологии:**
Python 3.7 <br>
Django 3.2 <br>
DRF 3.12.4 <br>
Docker Hub <br>
Github Actions <br>
djoser==2.1.0 <br>
PostgreSQL <br>
nginx <br>
gunicorn <br>
Yandex cloud 

---

### **Разработчик:**
- Вергасов Ришат <br>
- GitHub: https://github.com/Rishat-Ver <br>
- Telegram: https://t.me/Rishik1991 <br>
- Email: Zvezda-Rishat1991@yandex.ru <br>
- Вконтакте: https://vk.com/id356120934

---

### **Запуск проекта локально в контейнерах:**
```
git clone git@github.com:Rishat-Ver/foodgram-project-react.git # клонируем проект
python -m venv venv # Создаем виртуальное окружение
source /venv/Scripts/activate # Активируем виртуальное окружение
cd infra/ # Переходим в папку infra/
docker-compose up # Запуск docker-compose (Документация доступна по адресу http://localhost/api/docs/)
cd backend/ # Переходим в папку backend/ , сдесь мы пишем бек
django-admin startproject foodgram # Создаем основу проекта
python manage.py startapp api # Создаем приложение api
python manage.py startapp users # Создаем приложение users
python manage.py startapp recipes # Создаем приложение recipes
# ПИШЕМ ПРОЕКТ СОГЛАСНО ДОКУМЕНТАЦИИ
# ПРОВЕРЯЕМ ВСЕ РУЧКИ В POSTMAN
pip install gunicorn # Устанавливаем gunicorn
# Дописываем docker-compose.yaml
# Дописываем nginx.conf
docker compose up --build # Собираем образы и контейнеры
# Открываем второй терминал
docker ps # Смотрим какие контейнеры есть , выбираем backeyd(id-его)
docker exec -it 970a7bf530d0 bash # Попадаем внутрь контейнера 
python manage.py collectstatic # Собираем статику в контейнере
# ТЕСТИМ ПРОЕКТ ЛОКАЛЬНО ВНУТРИ РАБОТАЮЩИХ КОНТЕЙНЕРОВ
```

---

### **Запуск проекта на сервере в контейнерах:**


---

### **шаблон наполнения env-файла**

```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=rishik
DB_HOST=db
DB_PORT=5432
SECRET_KEY='django-insecure-ius$16a#%i7)4bk(gv)2w76)+!@3!*lxw3@hdgh^ah@1le&@6)'

```
---
### **Actions secrets**

```
DB_ENGINE
DB_HOST
DB_NAME
DB_PORT
DOCKER_PASSWORD
DOCKER_USERNAME
HOST
POSTGRES_PASSWORD
POSTGRES_USER
SECRET_KEY
SSH_KEY
TELEGRAM_TO
TELEGRAM_TOKEN
USER

```

---

### **Спецификация API Foodgram**
Документация: http://localhost/api/docs/

---

Данный проект , является дипломной работой начинающего програмиста Врегасова Ришата Ришатовича <br>
https://github.com/Rishat-Ver <br>
Он сделан в рамках обучения на курсе Python-рфзроботчик Яндекс-Практикума <br>
Backend разработкой, настройкой сервера , докера и т п работал Ришат Вергасов <br>
