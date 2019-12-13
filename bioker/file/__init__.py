import json
from pathlib import Path

from bioker.util.string import StringsMatchBuilder


def find_files_recursive(directory: str, pattern: str):
    return list(Path(directory).glob(pattern))


def get_strings_match_builder(directory: str, pattern: str):
    return StringsMatchBuilder(find_files_recursive(directory, pattern))


def get_file_content(file_path: str) -> str:
    with open(file_path, 'r') as f:
        return f.read()


def get_file_obj(file_path: str) -> dict:
    return json.loads(get_file_content(file_path))
