# DongCheDi Car Parser

Парсер для сайта DongCheDi, который позволяет получать информацию об автомобилях с пробегом, включая цены и изображения.

## Автор

**Spinej Andrej**  
Email: enjoyhillol@gmail.com

## Описание

Программа представляет собой GUI-приложение для парсинга данных об автомобилях с сайта DongCheDi. Извлекает следующую информацию:

-   Название и модель автомобиля
-   Текущую цену
-   Цену нового автомобиля
-   Размер экономии
-   Фотографии автомобиля

## Установка

1. Клонируйте репозиторий:

```bash
git clone https://github.com/Father1993/website-parser-dongchedi.git
cd website-parser-dongchedi
```

2. Создайте виртуальное окружение и активируйте его:

```bash
python -m venv venv
source venv/bin/activate # для Linux/Mac
venv\Scripts\activate # для Windows
```

3. Установите зависимости:

```bash
pip install -r requirements.txt
```

4. Установите браузер для Playwright:

```bash
playwright install chromium
```

## Использование

1. Запустите программу:

```bash
python main.py
```

2. В открывшемся окне вставьте URL автомобиля с сайта DongCheDi.
3. Нажмите кнопку "Получить данные".
4. Дождитесь завершения парсинга.

Результаты сохраняются в папку `cars/[id_автомобиля]/`:

-   `info.json` - информация об автомобиле
-   `image_[N].webp` - фотографии автомобиля

## Структура проекта

```
website-parser-dongchedi/
├── main.py            # GUI приложение
├── parser.py          # Парсер сайта
├── requirements.txt   # Зависимости
└── cars/              # Папка с результатами
    └── [car_id]/      # Данные по каждому авто
```

## Зависимости

-   `playwright==1.41.2`
-   `requests==2.31.0`
-   `python-dotenv==1.0.0`
-   `tkinter` (встроен в Python)

## Лицензия

MIT License

## Дисклеймер

Программа создана в образовательных целях. Автор не несет ответственности за использование программы в коммерческих целях.
