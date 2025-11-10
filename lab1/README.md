# Лабораторная работа №1 

## Задача: 
Настроить nginx согласно тз

## 1 шаг. Подготовка к работе. Установка и базовая настройка Nginx
В первую очередь важно сказать, что тема для нас была давольно новой и малоизвестной, поэтому почти сразу же стало понятно, что с данной лабораторной работы придеться повозиться, и изучить всю информацию подробнее. 
В лабораторной работе необходимо сделать https-запрос, для этого необходимо иметь ssl-сертификат, и для реализации мы выбрали вариант с самоподписным сертификатом, что в целом подходит для учебный проектов и локальных северов

В первую очередь все началось с осознания, что вновь придется вернуться к уже забытому VNWare и любимому Linux (тоже марально сложный шаг). И сразуже затем тоже морально сложный шаг устанвоки и настройки в ожидание пройдет ли все гладко (спойлер - прошло, поэтому начинаю рассказывать все по шагам)

Цель этого этапа: запустить веб-сервер Nginx на Ubuntu, проверить, что он работает и доступен по HTTP

### Проверяем обновление системы
'''
sudo apt update && sudo apt urgrade -y
'''
Тут не рискуем, сразу же и проверяем и приводим систему к акутальному состоянияю, подтягивая все нужные пакеты

### Устанавливаем Nginx
```
sudo apt install nginx -y
sudo systemctl status nginx
```

Сразу же и устанавливаем и проверяем статус. Видем зеленую строку и радуемся что устанвока прошла успешно
<img width="844" height="405" alt="Screenshot from 2025-11-10 15-22-47" src="https://github.com/user-attachments/assets/915ac90d-abd6-4712-acc0-1b2e112ecf4a" />

### Проверяем работу локально
Открываем браузер внутри виртуальной машины и вводим: 
```
http://localhost
```

и видем стандартную страницу приветстивя Nginx, значит все работает верно
<img width="868" height="516" alt="Screenshot from 2025-11-10 15-23-52" src="https://github.com/user-attachments/assets/efd5b3ab-62fe-4b26-9fcd-e162e1512e7d" />

### Проверяем работу с основного устройства
Этот шаг не обязателен, но чтобы в будущем не было сюрпризов проверяем все досконально.
Узнаем IP-адресс виртуалки:
```
ip a
```

На основном устройстве открываем браузер и вводим наш IP:
```
http://<IP>
```

и видим ту же страницу, что и в браузере на виртуальной машине, а это значит что все работает верно
<img width="1417" height="436" alt="Screenshot 2025-11-10 153221" src="https://github.com/user-attachments/assets/588df102-0f3f-4b3f-9eb4-f4b4f02a1673" />

### Разрешаем HTTP и HTTPS доступ
```
sudo ufw allow "Nginx Full"
sudo ufw enable 
sudo ufw status
```

Теперь Ubuntu разрешает входящие соединения по 80 и 443 портам

## Шаг 2. Создание проектов и их заполнение 

### Создаем корневые папки для проектов:
```
sudo mkdir -p /var/www/project_a /var/www/project_b
```
каждый проект - отдельный сайт
<img width="859" height="182" alt="Screenshot from 2025-11-10 16-30-19" src="https://github.com/user-attachments/assets/0801f508-cfa9-44ae-8e66-d08d4afc7994" />

### Создаем базовые HTML файлы 
```
sudo nano /var/www/project_a/index.html
```

Вставляем туда базовый код:
<img width="458" height="287" alt="Screenshot from 2025-11-10 16-33-42" src="https://github.com/user-attachments/assets/a8b1fad6-a6c3-474b-8a2c-d77f1fbe2c15" />

и также для второго проекта
<img width="532" height="287" alt="Screenshot from 2025-11-10 16-37-09" src="https://github.com/user-attachments/assets/7dbe08c8-cb0e-40c3-83e3-ba7db8e142c1" />

проверяем что файлы создались корректно:
<img width="822" height="512" alt="Screenshot from 2025-11-10 16-38-26" src="https://github.com/user-attachments/assets/8a250b84-3c5e-4cbc-94ce-f3bc32a096fa" />

### Настройка прав доступа

Меняем владельцев файлы на www-data, потому что если владельцем будет root или другой пользователь, Nginx может не иметь права читать файлы

```
sudo chown -R www-data:www-data /var/www/project_a
sudo chown -R www-data:www-data /var/www/project_b
```

и выполняем проверку, где видем что владельцем и группой для всех файловв является www-data, что мы и хотели сделать

<img width="902" height="112" alt="Screenshot from 2025-11-10 16-45-02" src="https://github.com/user-attachments/assets/6cfa895f-edc6-4a6d-8ae7-fcc19ab41c9a" />

### Установка прав доступа
```
sudo chmod -R 755 /var/www
```

* (7 для владельца) владелец может читать, писать и выполнять
* (5 для группы и остальных) группа и остальные могут читать и заходить в папку, но не редактировать

проверка:
```
ls -l /var/www/project_a
```

<img width="902" height="112" alt="Screenshot from 2025-11-10 16-45-02" src="https://github.com/user-attachments/assets/bb0d9f94-67ab-401b-aaba-a1e4f36e10ee" />

## Настройка виртуальных хостов

### Создаем конфиг для проекта A
```
sudo nano /etc/nginx/sites-available/project_a
```

в него пишем следующий код:
```
server {
    listen 80;  # слушаем HTTP-запросы на порту 80
    server_name project-a.local;  # домен для проекта A, nginx будет использовать для запросов эту конфигурацию

    root /var/www/project_a;
    index index.html index.htm;

    location / {
        try_files $uri $uri/ =404;  # проверяем наличие файла, если нет — 404
    }
}
```

### Создаем конфиг для проекта B
```
sudo nano /etc/nginx/sites-available/project_b
```

в него пишем код с похожим принципом как в проекте А, только с другим доменом и путем:
```
server {
    listen 80;  # слушаем HTTP-запросы на порту 80
    server_name project-b.local;  # домен для проекта A, nginx будет использовать для запросов эту конфигурацию

    root /var/www/project_b;
    index index.html index.htm;

    location / {
        try_files $uri $uri/ =404;  # проверяем наличие файла, если нет — 404
    }
}
```

### Активируем сайты
Создаем симвалические ссылки в sites-enabled, чтобы Nginx их увидел
```
sudo ln -s /etc/nginx/sites-available/project_a /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/project_b /etc/nginx/sites-enabled/
```

Здесь sites-available — хранилище всех конфигов, а sites-enabled — активные конфиги

Проверяем синтаксис и перезагружаем Nginx:
```
sudo nginx -t
```

Здесь видем вывод syntax is ok, значит у нас все работает верно 

Перезагружаем сервер:
```
sudo systemctl reload nginx
```

### настройка локальных доменов:
Чтобы тестировать наши сайты на локальной машине (основном устройстве)

```
sudo nano /etc/hosts
```

Добавляем строки, которые как раз таки указывают, что домены должны вести на локальную машину:
```
127.0.0.1 project-a.local
127.0.0.1 project-b.local
```
Проверка:
```
ping -c 2 project-a.local
ping -c 2 project-b.local
```

Здесь видим, что нам отвечаю, а это отдельный повод для радости, потому что значит все работает как надо и все пакеты доходят до цели

## Шаг 5. Настройка SSL сертификатов

### Создание папки для хранения сертификатов
```
sudo mkdir -p /etc/ssl/project_a
sudo mkdir -p /etc/ssl/project_b
```

### Генерация самоподписанного сертификата и ключа
Для проекта A:
```
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/ssl/project_a/project_a.key \
  -out /etc/ssl/project_a/project_a.crt
```
Common Name — project-a.local.

И тут надо разобраться поточнее:
* req -x509 создаёт самоподписанный сертификат
* -nodes означает доступ без пароля и ключа, иначе Nginx не сможет перезапускаться автоматически
* -days 365 это срок действия сертификата
* rsa:2048 — длина ключа.
* -keyout и -out пути для сохранения ключа и сертификата


Для проекта B аналогично:
```
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/ssl/project_b/project_b.key \
  -out /etc/ssl/project_b/project_b.crt
```

Common Name — project-b.local

## Настройка HTTPS-виртуальных хостов
Теперь добавим новые блоки серверов (или изменим старые) в /etc/nginx/sites-available

Открываем проект A и меняем содержимое:
```
# HTTP — перенаправляем на HTTPS
server {
    listen 80;
    server_name project-a.local;
    return 301 https://$host$request_uri;
}

# HTTPS
server {
    listen 443 ssl;
    server_name project-a.local;

    ssl_certificate /etc/ssl/project_a/project_a.crt;
    ssl_certificate_key /etc/ssl/project_a/project_a.key;

    root /var/www/project_a;
    index index.html index.htm;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

Аналогично для проекта B:
```
server {
    listen 80;
    server_name project-b.local;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name project-b.local;

    ssl_certificate /etc/ssl/project_b/project_b.crt;
    ssl_certificate_key /etc/ssl/project_b/project_b.key;

    root /var/www/project_b;
    index index.html index.htm;

    location / {
        try_files $uri $uri/ =404;
    }
}
```


