
import os
import pickle


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

def save_as_pickle(path, where_to_save_result):
    pkl_path = os.path.join(where_to_save_result, "directory_structure.pkl")
    with open(pkl_path, "wb") as file:
        pickle.dump(build_directory_tree(path), file)
