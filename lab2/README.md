# Лабораторная работа №2
## Цель работы
Изучение распространённых ошибок при создании Docker-образов и освоение лучших практик написания Dockerfile.

## Созданные файлы

### 1. Исходный код приложения
**app.py**:
```python
#!/usr/bin/env python3
import time
import sys

def main():
    print("Добро пожаловать!")
    
    counter = 0
    try:
        while counter < 5:
            counter += 1
            print(f"Итерация #{counter}: Приложение работает...")
            time.sleep(1)
        
        print("\nПриложение успешно завершило работу!")
        return 0
    except KeyboardInterrupt:
        print("\n\nПриложение остановлено пользователем")
        return 130

if __name__ == "__main__":
    sys.exit(main())
```

### 2. "Плохой" Dockerfile
**Dockerfile.bad**:
```dockerfile
FROM ubuntu:latest

RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN apt-get install -y curl
RUN apt-get install -y wget
RUN apt-get install -y vim
RUN apt-get install -y git

COPY . /app

RUN chmod -R 777 /app

CMD python3 /app/app.py
```

### 3. "Хороший" Dockerfile
**Dockerfile.good**:
```dockerfile
FROM python:3.11-slim

RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

COPY app.py .

RUN chown -R appuser:appuser /app

USER appuser

CMD ["python3", "app.py"]
```

## Плохие практики
### 1) **ubuntu:latest** - непредсказуемая версия, при пересборке через время может измениться
### 2) **Множественные RUN** - каждая инструкция RUN создает новый слой в образе, увеличивает размер
### 3) **Установка лишних пакетов** (curl, wget, vim, git) - не используются приложением, раздувают образ
### 4) **COPY . /app** - копирует всё, включая .git, README, временные файлы
### 5) **chmod 777 и запуск от root** - серьёзная проблема безопасности, нарушение принципа минимальных привилегий
### 6) **CMD в shell-формате** - неправильная обработка сигналов, проблемы при остановке контейнера

## Хорошие практики
### 1) **python:3.11-slim** - конкретная версия + компактный образ, Python уже установлен
### 2) **Создание непривилегированного пользователя** - повышает безопасность
### 3) **WORKDIR** - устанавливает рабочую директорию
### 4) **COPY app.py .** - копируется только нужный файл
### 5) **USER appuser** - запуск от обычного пользователя, не root
### 6) **CMD в exec-формате** - правильная работа с сигналами

## Соберем и запустим каждый Dockerfile:
```bash
docker build --no-cache -t docker-lab2-bad -f Dockerfile.bad .
docker build --no-cache -t docker-lab2-good -f Dockerfile.good .
docker run --rm docker-lab2-bad
docker run --rm docker-lab2-good
```

### Сравнение размеров:
```bash
docker images | grep docker-lab2
```

### Проверка безопасности:
```bash
docker run --rm docker-lab2-bad whoami   # root
docker run --rm docker-lab2-good whoami  # appuser
```

| Метрика | Плохой образ | Хороший образ |
|---------|--------------|---------------|
| Размер | ~180-200 MB | ~120-130 MB |
| Слои | 10+ слоёв | 5-6 слоёв |
| Безопасность | root | appuser |

## Плохие практики при работе с контейнерами
### 1) Хранение данных внутри контейнера
**Что конкретно плохо:** Все данные внутри контейнера (база данных, файлы пользователей, логи) безвозвратно теряются при удалении или пересоздании контейнера. Нужно использовать volumes.

**Правильно:**
```bash
docker volume create my-data
docker run -v my-data:/app/data my-app
```

### 2) Накопление остановленных контейнеров
**Что конкретно плохо:** После каждого запуска контейнер остаётся в системе со статусом Exited. Со временем накапливаются десятки мёртвых контейнеров, занимая дисковое пространство.

**Правильно:**
```bash
# Использовать флаг --rm для автоудаления
docker run --rm my-app

# Или регулярно чистить
docker container prune
```
