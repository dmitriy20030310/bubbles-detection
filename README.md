# Проект детекции спутников в космосе

## Описание проекта

Данный проект представляет собой систему для детекции спутников на изображениях космоса с использованием нейронных сетей. 

### Задача

Задача заключается в детекции спутников на изображениях космоса и определении их местоположения с помощью bounding boxes. Модель должна предсказывать координаты прямоугольника, ограничивающего спутник на изображении.

### Используемые технологии

- **YOLOv8** — детекция объектов
- **Ultralytics** — обучение и инференс
- **Hydra** - управление конфигурациями
- **DVC** - управление версиями данных
- **MLflow** — логирование экспериментов
- **FastAPI** - бэкенд
- **React** — фронтенд
- **Poetry** — управление зависимостями

## Структура репозитория

```bash
bubbles-detection/
├── core/                   # Основной код
│   ├── configs/            # Конфигурации Hydra
│   ├── weights/            # Директория для весов для работы app.py
│   ├── app.py              # FastAPI-сервер
│   ├── train.py            # Обучение модели
├── dataset/                # Датасет для обучения
├── service/                # React
├── pyproject.toml          # Зависимости проекта
├── .pre-commit-config.yaml # Конфигурация pre-commit
└── README.md               # Этот файл
```

## Setup

### Требования

- Python >= 3.12, < 3.14
- Poetry для управления зависимостями
- CUDA (опционально, для GPU ускорения)

### Установка окружения

1. Клонируйте репозиторий:
```bash
git clone https://github.com/DaniilMako/bubbles-detection
cd bubbles-detection
```

2. Создайте виртуальное окружение и установите зависимости:
```bash
# Создание виртуального окружения
python -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate

# Установка Poetry (если не установлен)
pip install poetry

# Установка зависимостей
poetry install
```

3. Установить npm
```bash
cd service
npm install
cd ..
```

4. Установите pre-commit хуки:
```bash
pre-commit install
```

5. Загрузите данные через DVC (опционально, см. dataset/README.md):
```bash
# Настройте DVC remote (если необходимо/нет .dvc)
dvc init
mkdir .dvc-storage
dvc remote add -d mylocal .dvc-storage

# Загрузите данные
dvc pull
```

6. Загрузите веса модели:
```bash
# Веса модели должны быть загружены/перемещены в weights/model.pt
dvc get https://huggingface.co/DaniilMako/bubbles-detection model.pt -o core/weights
```

## Train

### Обучение модели с логированием mlflow

Терминал 1:
```bash
mlflow ui --host 127.0.0.1 --port 8080
```

Терминал 2:
```bash
python core/train.py
```

### Конфигурация обучения

Основные параметры обучения настраиваются через Hydra конфиги в `core/configs/`:

- `config.yaml` - общая конфигурация
- `default.yaml` - конфигурация гиперпараметров
- `data.yaml` - конфигурация датасета
- `yolov8.yaml` - конфигурация модели yolov8
- `mlflow.yaml` - конфигурация логирования (MLflow)
- `api.yaml` - конфигурация api
### Логирование экспериментов

Эксперименты логируются в MLflow. Сервер MLflow должен быть запущен на `127.0.0.1:8080`:

```bash
mlflow ui --host 127.0.0.1 --port 8080
```

## Production preparation

Для запуска веб-интерфейса и использования модели необходимо:
1. Убедиться, что установлены все зависимости (см. Setup)
2. Переместить обученную модель в core/{paths.model_path}, по умолчанию core/weights/model.pt

## Infer

### Локальный инференс

Для запуска инференса на изображениях из директории:

```bash
cd service
npm start
```

React будет доступен на `http://localhost:3000`

### API сервер

Для запуска API сервера:

```bash
cd core
python app.py
```

API будет доступен на `http://localhost:8000`.

## Лицензия

MIT

## Авторы

Киль Д.
