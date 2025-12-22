# Лабораторная работа по классификации облачных сервисов №1 

Вариант 11

### Цель работы: 
Знакомство с облачными сервисами. Понимание уровней абстракции над инфраструктурой в облаке. Формирование понимания типов потребления сервисов в сервисной-модели


## Немного теории для выполнения лабораторной: 
В рамках лабораторной работы требуется проанализировать биллинговые данные облачного провайдера Amazon Web Services и выполнить классификацию потребляемых ресурсов по уровням абстракции, соответствующим моделям IaaS, PaaS и SaaS

Облачные провайдеры используют модель оплаты по факту потребления ресурсов

### Что такое IaaS, PaaS и SaaS
IaaS, PaaS и SaaS это все три основыне модели обслуживания облачных технологий

* IaaS предоставляет пользователю базовые инфраструктурные ресурсы, такие как виртуальные машины, хранилище и сетевые компоненты. Пользователь самостоятельно управляет операционной системой и установленным программным обеспечением
* PaaS предоставляет пользователю готовую платформу для разработки и размещения приложений, при этом управление инфраструктурой выполняется облачным провайдером (не думаем про сервер, просто размещаем приложение или базу данных)
* SaaS представляет собой готовое программное обеспечение, доступное пользователю через интернет, при котором облачный провайдер полностью управляет инфраструктурой и платформой (просто пользуемся программой)

# Выполнение работы:

### Импорт и разбор исходных данных
Первым делом испротируем .csv файл в Excel с разбиением точка с запятой

<img width="1256" height="932" alt="2025-12-22_23-13-05" src="https://github.com/user-attachments/assets/b237cbd3-688a-4dc0-9afa-0e9df1d4c0d8" />


это подготовительный шаг лабораторной, мы можем видеть нашу исходную таблицу с которой нам предстоит работать

В ходе лабораторной работе мы должны выполнить классификацию облачных ресурсов по иеархии: (это те колонки, что мы заполняем)
* IT Tower
* Service Family
* Service Type 
* Service Sub Type
* Service Usage Type

Заполненные колонки (исходные данные):
* productCode — указывает на конкретный облачный сервис Amazon Web Services
* usageType — отражает тип и характер потребления ресурса
* operation — описывает выполняемую операцию внутри сервиса
* lineItemDescription — текстовое описание потребляемого ресурса

На основе этих параметров выполняется сопоставление биллинговых данных с официальной документацией Amazon Web Servicesя

### Заполняем первые строки таблицы (вручную)
Первоначально классификация выполняется вручную для нескольких строк с целью понимания логики сопоставления биллинговых метрик с уровнями сервисной модели облачных вычислений

В качестве первого примера был рассмотрен сервис Amazon Athena. Данный сервис предоставляет возможность выполнения SQL-запросов к данным без управления инфраструктурой, что позволяет отнести его к модели PaaS. Биллинг сервиса осуществляется на основе объёма данных, считанных при выполнении запросов, что отражено в метрике DataScanned

<img width="1796" height="118" alt="2025-12-22_23-32-48" src="https://github.com/user-attachments/assets/99f5c8f7-17fe-4f0a-9c2b-6392f189ab20" />


В ходе выполнения лабораторной работы рассматривалась возможность автоматизации процесса классификации с использованием системы правил (mapping rules). Однако после анализа структуры исходных данных было принято решение выполнить классификацию вручную, опираясь на официальную документацию Amazon Web Servicesи ( https://docs.aws.amazon.com/ )

<img width="2034" height="1163" alt="image" src="https://github.com/user-attachments/assets/d8a11266-aaaf-49a4-9627-562d5cfc4058" />


# Классификация сервисов AWS по иерархии потребления
В рамках лабораторной работы было выполнено распределение потребления облачных сервисов AWS по иерархии, что позволяет анализировать использование ресурсов от общего уровня (IT Tower) до конкретного типа потребления (Service Usage Type)

## 1. Compute (Вычислительные ресурсы)


### Virtual Machines
Amazon Lightsail — сервис для запуска виртуальных серверов с преднастроенными ресурсами

Иерархия потребления:
Compute → Virtual Machines → Amazon Lightsail → Bundled virtual server

## 2. Data (Работа с данными)

### Analytics
Amazon Athena — управляемый сервис для выполнения SQL-запросов к данным без управления серверами

Иерархия потребления:
Data → Analytics → Amazon Athena → Serverless query service

### Storage
Amazon S3 (Simple Storage Service) — объектное хранилище данных

Иерархия потребления:
Data → Storage → Amazon S3 → Object storage

### Database
Amazon Neptune — управляемая графовая база данных

Иерархия потребления:
Data → Database → Amazon Neptune → Managed graph database

### Data Integration
AWS Glue — управляемый сервис для ETL и интеграции данных

Иерархия потребления:
Data → Data Integration → AWS Glue → Managed ETL service

## 3. Application Services (Сервисы приложений)

### Machine Learning
Amazon Machine Learning — управляемая платформа машинного обучения

Иерархия потребления:
Application Services → Machine Learning → Amazon Machine Learning → Managed machine learning service

### Artificial Intelligence
Amazon Lex — сервис для создания чат-ботов и голосовых интерфейсов

Иерархия потребления:
Application Services → Artificial Intelligence → Amazon Lex → Conversational AI service

### Blockchain
Amazon Managed Blockchain — управляемая платформа для работы с блокчейн-сетями

Иерархия потребления:
Application Services → Blockchain → Amazon Managed Blockchain → Managed blockchain service

### Application Streaming
Amazon AppStream 2.0 — сервис потоковой доставки приложений пользователям

Иерархия потребления:
Application Services → Application Streaming → Amazon AppStream 2.0 → Managed application streaming

## 4. Security (Безопасность)

### Data Security
Amazon Macie — сервис для обнаружения и защиты конфиденциальных данных

Иерархия потребления:
Security → Data Security → Amazon Macie → Sensitive data discovery service

## 5. Networking (Сетевые сервисы)

### Traffic Acceleration
AWS Global Accelerator — сервис для ускорения сетевого трафика

Иерархия потребления:
Networking → Traffic Acceleration → AWS Global Accelerator → Managed global traffic acceleration

## 6. Governance и Financial (Управление и финансы)

### Configuration Management
AWS Config — сервис для мониторинга конфигураций облачных ресурсов

Иерархия потребления:
Governance → Configuration Management → AWS Config → Configuration monitoring service

### Cost Management
AWS Cost Explorer — сервис анализа затрат на облачные ресурсы

Иерархия потребления:
Financial → Cost Management → AWS Cost Explorer → Cost analysis service

# Вывод
В результате выполнения лабораторной работы потребление облачных сервисов AWS было распределено по иерархии от общего уровня (Compute, Data, Security, Networking) до конкретных типов использования ресурсов. Такой подход позволяет проводить анализ потребления от крупных категорий к деталям и наглядно показывает, за какие именно действия и ресурсы формируется стоимость облачных сервисов
