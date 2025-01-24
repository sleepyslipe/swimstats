import pandas as pd
import os
import chardet

def delete_rows_by_competition_name(file_path, competition_name_to_delete):
    """
    Считывает данные из CSV-файла, удаляет строки, где в столбце 'competition_name'
    есть значение competition_name_to_delete, и сохраняет изменения обратно в файл.

    Args:
        file_path (str): Путь к CSV-файлу.
        competition_name_to_delete (str): Название соревнования, строки с которым нужно удалить.
    """
    try:
        # Читаем CSV-файл, определяем кодировку и используем ее
        with open(file_path, 'rb') as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            encoding = result['encoding']
        if encoding:
            df = pd.read_csv(file_path, encoding=encoding)
        else:
            df = pd.read_csv(file_path, encoding='utf-8')

        # Фильтруем строки, исключая строки со значением 'Кубок России 2024' в столбце 'competition_name'
        df = df[df['competition_name'] != competition_name_to_delete]

        # Перезаписываем CSV-файл с изменениями, без индекса, в UTF-8
        df.to_csv(file_path, index=False, encoding='utf-8')

        print(f"Строки с '{competition_name_to_delete}' в столбце 'competition_name' были успешно удалены из '{file_path}'")

    except FileNotFoundError:
        print(f"Ошибка: Файл '{file_path}' не найден.")
    except KeyError:
        print(f"Ошибка: Столбец 'competition_name' не найден в файле '{file_path}'.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    file_path = 'sources/results_dataframe.csv' # Замените на путь к вашему CSV-файлу
    competition_name_to_delete = 'Кубок России 2024'

    if os.path.exists(file_path) and os.path.getsize(file_path) > 0: #проверка что файл не пустой
        delete_rows_by_competition_name(file_path, competition_name_to_delete)
    else:
        print(f"Файл '{file_path}' не найден, либо он пустой.")