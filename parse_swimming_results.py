import re # библиотека для регулярных выражений
import csv
from datetime import datetime
import PyPDF2
import chardet
import pandas as pd
from enum import Enum
import os
import json


input_file = 'sources/competitions_lists/test2.json'

print('Script started')
output_results_file_path = 'sources/test2.csv'

# создание словаря с именами столбцов будущего датафрейма и типами данных
column_types = {
    'competition_id': 'int64',
    'date': 'datetime64[ns]',
    'distance': 'int64',
    'style': 'string',
    'age_category': 'string',
    'athlete': 'string',
    'sex': 'string',
    'age': 'int64',
    'club': 'string',
    'time': 'float64',
    'points': 'int64',
    'place': 'int64'
}


# создание датафрейма, который будет хранить данные о результатах заплывов
results_dataframe = pd.DataFrame(columns=column_types.keys()).astype(column_types)

# класс, хранящий статусы чтения файла
class ReadingStatus(Enum):
    READING_STARTED = 1 # чтение начато (стартовый статус)
    DISTANCE_READ = 2 # прочитана строка с дистанцией: длина дистанции, стиль, м/ж, возрастная категория
    DATE_READ = 3 # прочитана строка с датой
    RESULT_READ = 4 # прочитана строка с результатом: место, фамилия и имя спортсмена, возраст, клуб, время (результат), набранные очки


# класс для корректного изменения статуса чтения
class ReadingProgress:
    # инициализация
    def __init__(self): 
        # стартовый статус - READING_STARTED
        self.current_status = ReadingStatus.READING_STARTED
        # порядок установления статусов в первый раз 
        # (статусы могут устанавливаться только в указанном ниже порядке, пока не будет установлен впервые статус RESULT_READ,
        #  после этого статусы могут устнавливаться в любом порядке)
        self.status_order = [
            ReadingStatus.READING_STARTED,
            ReadingStatus.DISTANCE_READ,
            ReadingStatus.DATE_READ,
            ReadingStatus.RESULT_READ
        ]
        # флаг достижения статуса RESULT_READ; изначально - False
        self.result_read_reached = False

    # метод установления нового статуса
    def set_status(self, new_status: ReadingStatus):
        # Если RESULT_READ был установлен, то разрешаем любые переходы
        if self.result_read_reached: 
            self.current_status = new_status
            return

        # устанавливает новый статус только в том случае, если он следующий в последовательности
        try:
            # находим индекс текущего статуса в списке статусов self.status_order
            # если текущего статуса нет в списке, возникает исключение ValueError
            current_index = self.status_order.index(self.current_status)
            next_index = current_index + 1
            # проверяем, что next_index находится в пределах списка status_order,
            # и что следующий статус в списке равен new_status
            if next_index < len(self.status_order) and self.status_order[next_index] == new_status:
                self.current_status = new_status
                # если достигли RESULT_READ, то устанавливаем флаг
                if new_status == ReadingStatus.RESULT_READ:
                   self.result_read_reached = True
        # просто ничего не делаем, если статус нельзя установить
        except ValueError as e:
            pass

    # метод, возвращающий True, если текущий статус - RESULT_READ, и False - если любой другой 
    def is_result_read(self) -> bool:
        return self.current_status == ReadingStatus.RESULT_READ


# функция, которая парсит pdf-файл с результатами и записывает данные в датафрейм results_dataframe
def parse_pdf_swimming_results(competition):

    # инициализируем процесс чтения файла, устанавливаем статус READING_STARTED
    progress = ReadingProgress()

    # считываем текст из pdf-файла и записываем в full_text
    full_text = ""
    try:
      with open(competition['input_file_path'], 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            full_text += page.extract_text()
    except Exception as e:
       print(f"Ошибка при открытии или чтении PDF-файла: {e}")
       return
    
    # паттерны для извлечения данных из строк разных типов: дата/результат/дистанция
    date_pattern = r"(\d{2}.\d{2}.\d{4})"
    result_pattern = r"(\d+)\.(\w+\s+\w+)\s+(\d+)\s+(\w+)\s*([\w\s-]*)\s+([\d:\.]+)\s+([0-9]{3,4})"
    race_pattern = r"(Женщины|Мужчины)\s+,\s+(\w+)m\s+(\w+)\s+(\w+\s)?(\d+\s-\s\d+)"
    age_category_pattern = r"(\d+\s-\s\d+)"

    # определяем кодировку текста
    raw_text = full_text.encode('utf-8', errors='ignore')
    result = chardet.detect(raw_text)
    encoding = result['encoding']
    if encoding:
       full_text = raw_text.decode(encoding, errors='replace')
    else:
        full_text = raw_text.decode('utf-8', errors='replace')
    
    # построчно считываем full_text
    for line in full_text.splitlines():

        line = line.strip()

        # если строка начинается с 1.ФАМИЛИЯ
        if re.search(r"^\d{1,2}\.[а-яА-Я]{2,}", line):
          # используем паттерн result_pattern
          match = re.search(result_pattern, line)

          if match:
            # устанавливаем статус RESULT_READ
            progress.set_status(ReadingStatus.RESULT_READ)

            # сохраняем в переменных место, фамилию и имя атлета, возраст, клуб, время (результат), набранные очки
            place = int(match.group(1))
            athlete = match.group(2)
            age = int(match.group(3))
            club = match.group(4)
            if match.group(5):
              if match.group(5)[0] != '-':
                club += ' ' 
              club += match.group(5)
            time = match.group(6)
            points = match.group(7)

        # если строка содержит Дистанция
        elif "Дистанция" in line:
          # используем паттерн race_pattern
          match = re.search(race_pattern, line)
          
          if match:
            # устанавливаем статус DISTANCE_READ
            progress.set_status(ReadingStatus.DISTANCE_READ)

            # сохраняем в переменных пол, дистанцию (длину в метрах), стиль, возрастную категорию
            if match.group(1) == 'Женщины':
              sex = 'ж'
            else:
              sex = 'м'
            distance = int(match.group(2))
            style = match.group(3)
            if match.group(4):
              style += ' ' + match.group(4)  
            # age_category = match.group(5)  

        # если строка содержит Результаты
        elif "Результаты" in line:
            # используем паттерн date_pattern
            match = re.search(date_pattern, line)

            if match:
              # устанавливаем статус DATE_READ
              progress.set_status(ReadingStatus.DATE_READ)
              # сохраняем в переменной дату
              date = match.group(1)

        elif "лет" in line and "моложе" not in line:
           match = re.search(age_category_pattern, line)
           if match:
              age_category = match.group(1)  
           
           

        # если текущий статус - RESULT_READ, вносим полученные данные в словарь new_row_data
        if progress.is_result_read():
          new_row_data = {
            'competition_id': competition['competition_id'],
            'date':  date,
            'distance': distance,
            'style': style,
            'age_category': age_category,
            'athlete': athlete,
            'sex': sex,
            'age': age,
            'club': club,
            'time': time,
            'points': points,
            'place': place
          }


          # добавляем в датафрейм новую строку - new_row_data
          if new_row_data['age'] >= 20:
            results_dataframe.loc[len(results_dataframe)] = new_row_data

          if len(results_dataframe)%100 == 0:
            print(f'{len(results_dataframe)} lines entered')

# список соревнований
with open(input_file, "r", encoding="utf-8") as f:
    competitions = json.load(f)

for comp in competitions:
   # вызов функции (загрузка данных в датафрейм)
   parse_pdf_swimming_results(comp)
   # удаление дубликатов и перезапись индексов
   results_dataframe = results_dataframe.drop_duplicates().reset_index(drop=True)


# создание файла результатов, если отсутствует, и добавление данных к файлу, если файл существует
if os.path.exists(output_results_file_path) and os.path.getsize(output_results_file_path) > 0:
    header = False
    mode = 'a'
else:
    header = True
    mode = 'w'

# загрузка данных в csv файл
try:
    results_dataframe.to_csv(
        path_or_buf=output_results_file_path,
        sep=',',
        na_rep='',
        header=header,
        index=False,
        mode=mode,
        encoding='windows-1251',
        compression='infer',
        quotechar='"',
        doublequote=True,
        decimal='.',
        errors='strict',
    )
    print(f"Данные успешно загружены в файл: {output_results_file_path}")
except Exception as e:
    print(f"Ошибка при записи в CSV-файл: {e}")

results_dataframe = None