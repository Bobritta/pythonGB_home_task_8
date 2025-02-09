# Напишите функцию, которая получает на вход директорию и рекурсивно обходит её и все вложенные директории.
# Результаты обхода сохраните в файлы json, csv и pickle.
#  Для дочерних объектов указывайте родительскую директорию.
#  Для каждого объекта укажите файл это или директория.
#  Для файлов сохраните его размер в байтах, а для директорий размер файлов в ней с учётом всех вложенных файлов и директорий.
# 3. Соберите из созданных на уроке и в рамках домашнего задания функций пакет для работы с файлами разных форматов.

from pathlib import Path
from sys import argv
import os

import csv_serialization
import json_serialization
import pkl_serialization

def show_what_is_inside (directory, where_to_save_result):
    """
    Функция получает на вход директорию и рекурсивно обходит её и все вложенные директории.
    Результаты обхода сохраняет в файлы json, csv и pickle.
    """
    if not Path(where_to_save_result).exists() or not Path(where_to_save_result).is_dir():
        os.mkdir(where_to_save_result)
    if not Path(directory).exists() or not Path(directory).is_dir():
        print("Неверно указан путь. Попробуйте снова.")
    else:
        json_serialization.save_as_json(directory, where_to_save_result)
        csv_serialization.save_as_csv(directory, where_to_save_result)
        pkl_serialization.save_as_pickle(directory, where_to_save_result)


if __name__ == '__main__':
    if len(argv) > 1:
        directory = argv[1]
    else:
        directory = Path('../directory_for_walking_task').resolve()
    if len(argv) > 2:
        where_to_save_result = argv[2]
    else:
        where_to_save_result = Path('../final_results').resolve()
    show_what_is_inside(directory, where_to_save_result)
