
import os
import csv


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