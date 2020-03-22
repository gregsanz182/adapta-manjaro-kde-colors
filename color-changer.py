import json
import os

from binaryornot.check import is_binary

JSON_PARAMS_FILE = "params.json"


def main():
    params = load_json_params()
    for directory_target in params["directories"]:
        list_of_files = get_list_of_files(directory_target)
        for file_target in list_of_files:
            if not is_binary(file_target):
                file_string = load_file_string(file_target)
                new_file_string = replace_colors(
                    file_string, params["replacements"])
                save_string(new_file_string, file_target)


def load_json_params():
    params = []
    with open(JSON_PARAMS_FILE, "r") as json_file:
        params = json.load(json_file)
    return params


def load_file_string(file_path):
    file_string = ""
    with open(file_path, "r") as file_target:
        print(file_path)
        file_string = file_target.read()
    return file_string


def replace_colors(string, replacements):
    replacement_pairs = get_replacement_pairs(replacements)
    new_string = string
    for pair in replacement_pairs:
        new_string = new_string.replace(pair[0].lower(), pair[1].lower())
    return new_string


def get_list_of_files(directory):
    files_list = []
    for dir_name, _, dir_files in os.walk(directory):
        files_list.extend(
            [os.path.join(dir_name, file_name) for file_name in dir_files])
    return files_list


def get_replacement_pairs(replacements):
    pairs = []
    for replace_string in replacements:
        hex_replace = replace_string.split(":")
        pairs.append(hex_replace)
        pairs.append([
            hex_to_rgb(hex_replace[0]),
            hex_to_rgb(hex_replace[1])
        ])
    return pairs


def save_string(string, file_path):
    with open(file_path, "w") as file_target:
        file_target.write(string)


def hex_to_rgb(hex_string):
    hex_string_stripped = hex_string.lstrip("#")
    return ",".join(
        str(int(hex_string_stripped[i:i+2], 16)) for i in (0, 2, 4))


if __name__ == "__main__":
    main()
