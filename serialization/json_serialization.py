
import os
import json


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
