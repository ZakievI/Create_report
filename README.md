# Генератор отчетов по зарплатам сотрудников

Проект для обработки CSV-файлов с информацией о сотрудниках и автоматического расчета их заработной платы.

## 📋 Возможности

- 📂 Чтение данных сотрудников из одного или нескольких CSV-файлов
- 🧮 Автоматический расчет зарплаты (payout) на основе:
  - Отработанных часов
  - Почасовой ставки
- 🔄 Поддержка различных вариантов названий столбцов
- 📊 Форматированный вывод отчетов с группировкой по отделам
- ❌ Обработка ошибок и пропущенных данных

## ⚙️ Требования

- Python 3.6 и выше

## 🛠️ Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/ZakievI/Create_report
cd Create_report
```

## ✏️Использование
1. Формат входных данных
Поддерживаются CSV-файлы со следующими данными:
```sh
name,department,hours_worked,hourly_rate
Имя,Отдел,Часы,Ставка
```
2. Поддерживаемые названия столбцов:

- Для часов работы: hours_worked, hours
- Для ставки: hourly_rate, rate, salary
## 🚀Запуск программы
Базовый синтаксис:
```bash
python main.py файл1.csv [файл2.csv ...] --report payout
```
Пример:
```bash
python main.py data\\data1.csv data\\data2.csv data\\data3.csv --report payout
```
Пример вывода программы:
```sh
   name        hours_worked hourly_rate payout 
IT
-- John Doe    160          25          4000
-- Bob Johnson 180          20          3600
HR
-- Jane Smith  120          30          3600
```
## 🧪 Тестирование
Для запуска тестов необходимо установить несколько библиотек
```bash
pip install pytest pytest-cov
```
Далее запустите тесты
```bash
pytest --cov=main test_main.py -v
```
Для генерации HTML-отчета о покрыт
```bash
pytest --cov=main --cov-report=html test_main.py
```
