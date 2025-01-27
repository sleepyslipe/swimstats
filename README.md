![Swimstats](SwimCup.jpg)
# Swimstats результатов заплывов кубка России по плаванию 2024 г. (Мастерс)

Этот проект автоматизирует процесс извлечения данных о результатах заплывов кубка России по плаванию 2024 г. в группе Мастерс из PDF-файлов и последующей загрузки этих данных в базу данных.  Полученные данные затем визуализируются с помощью Streamlit для удобного просмотра и анализа.

## Цели проекта:

* **Автоматизация парсинга:**  Создать скрипт на Python, который автоматически извлекает данные о результатах заплывов из PDF-файлов кубка.  Это избавляет от ручного ввода данных, что значительно экономит время и снижает вероятность ошибок.
* **Хранение данных в базе данных:**  Загрузить извлеченные данные в реляционную базу данных (например, PostgreSQL, MySQL, SQLite) для долговременного хранения и удобного доступа.
* **Визуализация результатов:**  Разработать веб-приложение, например с использованием Streamlit для отображения результатов.  Приложение должно предоставлять интерактивный интерфейс для фильтрации и сортировки данных, а также для построения графиков и диаграмм.

## Архитектура проекта:

Проект состоит из трех основных частей:

1. **Парсер (Parser):**  Модуль на Python, отвечающий за извлечение данных из PDF-файлов.  Он использует библиотеки для работы с PDF, например такие как `PyPDF2`, `camelot`, `tika`, или `pdfplumber`,  выбор библиотеки зависит от структуры PDF-файлов.
2. **Загрузка в базу данных (Database Loader):**  Модуль, который подключается к базе данных и загружает в нее извлеченные парсером данные.  Для работы с базой данных используются библиотеки, такие как `psycopg2` (для PostgreSQL), `mysql.connector` (для MySQL), или `sqlite3` (для SQLite).
3. **Веб-приложение (Streamlit App):**  Веб-приложение на Streamlit для визуализации данных.  Данные загружаются из базы данных и отображаются с помощью интерактивных элементов Streamlit, позволяющих пользователю фильтровать, сортировать данные и строить графики.

## Технологии:

* **Python:** Язык программирования.
* **PyPDF2/camelot/tika/pdfplumber:** Библиотеки для парсинга PDF-файлов.
* **PostgreSQL/MySQL/SQLite:** Система управления базами данных (СУБД).
* **psycopg2/mysql.connector/sqlite3:** Библиотеки для работы с СУБД.
* **Streamlit:** Библиотека для создания веб-приложений.

## Инструкция по запуску:

... Пошаговая инструкция по запуску проекта, включая установку зависимостей, настройку базы данных и запуск скриптов.

Пример:

1.  `pip install -r requirements.txt`
2.  `python parser.py`  (запуск парсера)
3.  `python db_loader.py` (загрузка данных в базу данных)
4.  `streamlit run app.py` (запуск веб-приложения)

## Выводы:

Этот проект демонстрирует эффективность автоматизации задач обработки данных.  Автоматический парсинг PDF-файлов и загрузка данных в базу данных существенно ускоряют обработку информации и снижают вероятность ошибок.  Интерактивное веб-приложение на Streamlit обеспечивает удобный доступ к данным и позволяет проводить быстрый анализ результатов заплывов чемпионата.  В дальнейшем проект можно расширить, добавив функциональность для сравнения результатов участников разных возрастов, построения рейтингов и т.д.


## Будущие улучшения:

* Добавление возможности обработки различных форматов PDF-файлов.
* Реализация более сложной системы фильтрации и сортировки данных в веб-приложении.
* Интеграция с внешними API для получения дополнительной информации о спортсменах.
* Автоматизация загрузки PDF файлов, например, с помощью расписания.
* Построение более сложных визуализаций данных (например, heatmaps).
