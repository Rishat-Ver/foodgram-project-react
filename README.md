# Проект **Foodgram - "Продуктовый помощник"**
![example workflow](https://github.com/Rishat-Ver/foodgram-project-react/actions/workflows/footgram.yml/badge.svg)

---
### **Адрес проекта**
http://84.252.143.251/admin/  Админка<br>
http://84.252.143.251/api/docs/ Документация<br>
http://84.252.143.251/signin Вход на сайт и регистрация<br>
http://84.252.143.251/recipes Главная страница рецептов<br>
http://84.252.143.251/subscriptions Подписки<br>
http://84.252.143.251/recipes/create Создание рецепта<br>
http://84.252.143.251/favorites Избранное<br>
http://84.252.143.251/cart Список покупок

---

### **Тестовый пользователь и админ**
Пользователь:
```
Имя: Ринатка
Фамилия: Бикулова
Имя пользователя: Rinatka
Адрес электронной почты: rinatka1991@mail.ru
Пароль: 1991bik1991
```
Админ:
```
Имя: admin
Фамилия: admin
Имя пользователя: admin
Адрес электронной почты: admin@admin.ru
Пароль: admin
```

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
### **Команды докера**
```
docker-compose up --build
docker-compose down -v
docker images
docker ps
docker exec -it f5f5ed69e732 bash
docker build -t rishat1991/foodgram_frontend .
docker push rishat1991/foodgram_frontend
```
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
```
# МЕНЯЕМ БАЗУ SQLITE НА POSTGRES
pip install python-dotenv
# ИЗМЕНЯЕМ НАСТРОЙКИ БД В settings.pe
docker build -t rishat1991/foodgram_frontend . # Собрали образ foodgram_frontend
docker build -t rishat1991/foodgram_backend . # Собрали образ foodgram_backend
docker push rishat1991/foodgram_frontend # Запушили DockerHub
docker push rishat1991/foodgram_backend # Запушили DockerHub
ssh rishat@84.252.143.251 # Заходим на ВМ
mkdir Dev # Создаем директорию Dev
cd Dev/ # Переходим Dev
mkdir footgram # Создаем директорию footgram
scp -r infra rishat@84.252.143.251:/home/rishat/Dev/foodgram # Копируем infra/ на сервер
scp -r docs rishat@84.252.143.251:/home/rishat/Dev/foodgram # Копируем docs/ на сервер
# ПИШЕМ foodgram.yml
sudo systemctl stop nginx
git add .
git commit -m""
git push
```

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

Данный проект , является дипломной работой  начинающего програмиста Врегасова Ришата Ришатовича <br>
https://github.com/Rishat-Ver <br>
Он сделан в рамках обучения на курсе Python-рфзроботчик Яндекс-Практикума <br>
Backend разработкой, настройкой сервера , докера и т п работал Ришат Вергасов <br>
![2021-12-10 20-14-18](https://github.com/Rishat-Ver/foodgram-project-react/assets/113997223/8d98b2d1-a33b-4f20-823f-7656ae0dd5ac)
