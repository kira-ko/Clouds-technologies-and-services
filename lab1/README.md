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

## Шаг 3. Настройка виртуальных хостов

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
<img width="807" height="335" alt="Screenshot from 2025-11-10 20-16-38" src="https://github.com/user-attachments/assets/25c709f1-06f9-402d-a0a2-9abbbf71a02c" />


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
<img width="862" height="94" alt="Screenshot from 2025-11-10 20-20-07" src="https://github.com/user-attachments/assets/7ceddcda-00f7-4d4c-89a2-664b5f9f3c92" />

Здесь видем вывод syntax is ok, значит у нас все работает верно 

Перезагружаем сервер:
```
sudo systemctl reload nginx
```



### Настройка локальных доменов:
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

<img width="862" height="277" alt="Screenshot from 2025-11-10 20-21-20" src="https://github.com/user-attachments/assets/95c557a0-3d32-41f7-abab-e4d001513259" />


<img width="862" height="362" alt="Screenshot from 2025-11-10 20-22-26" src="https://github.com/user-attachments/assets/1b43f651-e4e0-4e8e-b8e6-c16b0a3af182" />

Здесь видим, что нам отвечают, а это отдельный повод для радости, потому что значит все работает как надо и все пакеты доходят до цели

## Шаг 4. Настройка SSL сертификатов

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


<img width="1029" height="423" alt="Screenshot from 2025-11-10 20-29-38" src="https://github.com/user-attachments/assets/373a6dc5-a21c-4489-be08-ecbaefc50d84" />


Для проекта B аналогично:
```
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/ssl/project_b/project_b.key \
  -out /etc/ssl/project_b/project_b.crt
```

Common Name — project-b.local

<img width="1029" height="515" alt="Screenshot from 2025-11-10 20-36-50" src="https://github.com/user-attachments/assets/4ca8eb64-1ed0-4882-8b5f-e7f64a0d0f35" />


## Шаг 5. Настройка HTTPS-виртуальных хостов
Теперь добавим новые блоки серверов (или изменим старые) в /etc/nginx/sites-available

# Открываем проект A и меняем содержимое:
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

<img width="647" height="515" alt="Screenshot from 2025-11-10 20-41-35" src="https://github.com/user-attachments/assets/950317b6-c0f7-4bdb-8e98-b74eed8e4488" />



# Аналогично для проекта B:
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

<img width="647" height="515" alt="Screenshot from 2025-11-10 20-42-38" src="https://github.com/user-attachments/assets/6e7da0fe-db9d-4a0d-ba15-ede39ef4a65a" />

Делаем вновь проверку, чтобы все работало корректно, радуемся что это так и делаем перезапуск:
```
sudo nginx -t
sudo systemctl reload nginx
```

<img width="862" height="94" alt="Screenshot from 2025-11-10 20-20-07" src="https://github.com/user-attachments/assets/86260576-a5b4-4c81-a991-38125f30069a" />


# Проверка работы HTTPS
Открываем в браузере два наших проекта:
* https://project-a.local
* https://project-b.local

Браузер конечно же показывает предупреждение, но мы доверяем своим же проектам, поэтому можем увидеть, что и проект А и проект В запускаются коректно!


# Проект А:
<img width="1004" height="665" alt="Screenshot from 2025-11-10 20-46-30" src="https://github.com/user-attachments/assets/292d8de3-3ed4-4f84-9f95-15e21f584aea" />

<img width="1004" height="665" alt="Screenshot from 2025-11-10 20-46-19" src="https://github.com/user-attachments/assets/2714873c-1c56-4f7c-8131-bd07e71fd80c" />

# Проект В:
<img width="1209" height="721" alt="Screenshot from 2025-11-10 20-47-08" src="https://github.com/user-attachments/assets/62ce4eed-8fd4-4547-8c2d-b23fc9c0de44" />

<img width="847" height="277" alt="Screenshot from 2025-11-10 20-47-20" src="https://github.com/user-attachments/assets/9a05b121-77e8-4de2-87f9-5b558312426d" />

## Шаг 6. Нстройка принудительного редиректа с HTTP на HTTPS

### Изменяем конфиг проекта А
Добавляем новый блок, отвечающий за редирект с HTTP на HTTPS

```
# --- HTTP -> HTTPS redirect ---
server {
    listen 80;
    server_name project-a.local;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name project-a.local;

    ssl_certificate /etc/nginx/ssl/project-a.crt;
    ssl_certificate_key /etc/nginx/ssl/project-a.key;

    root /var/www/project_a;
    index index.html index.htm;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

### То же самое для проекта B
```
# --- HTTP -> HTTPS redirect ---
server {
    listen 80;
    server_name project-b.local;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name project-b.local;

    ssl_certificate /etc/nginx/ssl/project-b.crt;
    ssl_certificate_key /etc/nginx/ssl/project-b.key;

    root /var/www/project_b;
    index index.html index.htm;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

### Проверим конфигурацию
```
sudo nginx -t
```

Все работает коректно

### Проверяем результат
Теперь надо првоерить работает ли наш редирикт, для этого откроем каждый сайт как http и автоматически должно перекинуть на https

Видим что редирикт работает

## Настройка Alias
Перед тем, как настроить alias немного видоизменим наши проекты, добавив картинку в каждый. Для этого мы заранее создавали папку для изображений в каждом проекте, сейчас сюда загружаем наши изображения

Сам Alias это механизм в Nginx, который позволяет создать виртуальный путь, указывающий на реальную директорую на сервере, позволяет создавать короткие URL вместо длинных и сложных, что удобно для статических файлов

### Для проекта А
Открываем и добавлем новый блок location для alias
```
location /pics_a/ {
    alias /var/www/project_a/static/images/;
}
```

### Для проекта B все в целом то же самое 
```
location /pics_b/ {
    alias /var/www/project_b/static/images/;
}
```

### Проверяем синтаксис Nginx + перезагрузка
```
sudo nginx -t
sudo systemctl reload nginx
```

### Обновляем HTML для использования alias
Теперь в файле index.html каждого проекта заменяем путь к картинкам

для проекта А:
```
<img src="/pics_a/cat.jpg" alt="Cat">
```

Для проекта B:
```
<img src="/pics_b/dog.jpg" alt="Dog">
```

## Обзор наших двух готовых проектов

### проект A:

### Проект B:


