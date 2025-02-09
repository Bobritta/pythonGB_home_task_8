# Напишите функцию, которая получает на вход директорию и рекурсивно обходит её и все вложенные директории.
# Результаты обхода сохраните в файлы json, csv и pickle.
#  Для дочерних объектов указывайте родительскую директорию.
#  Для каждого объекта укажите файл это или директория.
#  Для файлов сохраните его размер в байтах, а для директорий размер файлов в ней с учётом всех вложенных файлов и директорий.
# 3. Соберите из созданных на уроке и в рамках домашнего задания функций пакет для работы с файлами разных форматов.

from pathlib import Path
from sys import argv
import os
import json
import csv
import pickle

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
        save_as_json(directory, where_to_save_result)
        save_as_csv(directory, where_to_save_result)
        save_as_pickle(directory, where_to_save_result)


def build_directory_tree(path):
    tree = {"directories": {}, "files": [], "size": 0}
    entries = os.listdir(path)
    for entry in entries:
        full_path = os.path.join(path, entry)
        if os.path.isdir(full_path):
            sub_tree = build_directory_tree(full_path)
            tree["directories"][entry] = sub_tree
            tree["size"] += sub_tree["size"]
        else:
            file_size = os.path.getsize(full_path)
            tree["files"].append(f'{entry} {file_size} байт')
            tree["size"] += file_size

    return tree


def save_as_json(path, where_to_save_result):
    json_path = os.path.join(where_to_save_result, "directory_structure.json")
    with open(json_path, "w", encoding="utf-8") as json_file:
        json.dump(build_directory_tree(path), json_file, indent=4, ensure_ascii=False)


def build_directory_matrix(path):
    matrix = [['nesting level', 'name', 'dirs', 'files']]

    def sneek_inside(path):
        entries = os.listdir(path)
        dirs = []
        files = []

        for entry in entries:
            entry_full_path = os.path.join(path, entry)
            nesting_level = get_nesting_level (entry_full_path)
            if os.path.isdir(entry_full_path):
                size = 0
                for item in os.scandir(entry_full_path):
                    size += item.stat().st_size
                dirs.append(f'{entry} {size} байт')
                sneek_inside(entry_full_path)
            else:
                files.append(f'{entry} {os.path.getsize(entry_full_path)} байт')

        matrix.append([nesting_level, path, dirs, files])

    sneek_inside(path)
    matrix[1:] = sorted(matrix[1:], key=lambda x: x[0])
    return matrix


def get_nesting_level(path):
    components = path.split(os.sep)
    return len(components) - 2


def save_as_csv(path, where_to_save_result):
    csv_path = os.path.join(where_to_save_result, "directory_structure.csv")
    with open(csv_path, "w", newline='', encoding="utf-8") as csv_file:
        csv_write = csv.writer(csv_file, dialect='excel', delimiter=' ', quotechar='|', quoting = csv.QUOTE_MINIMAL)
        for line in (build_directory_matrix(path)):
            csv_write.writerow(line)


def save_as_pickle(path, where_to_save_result):
    pkl_path = os.path.join(where_to_save_result, "directory_structure.pkl")
    with open(pkl_path, "wb") as file:
        pickle.dump(build_directory_tree(path), file)

if __name__ == '__main__':
    if len(argv) > 1:
        directory = argv[1]
        if len(argv) > 2:
            where_to_save_result = argv[2]
        else:
            where_to_save_result = 'final_results'
        show_what_is_inside(directory, where_to_save_result)
