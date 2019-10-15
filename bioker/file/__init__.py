from pathlib import Path

from bioker.util.string import StringsMatchBuilder


def find_files_recursive(directory: str, pattern: str):
    return list(Path(directory).glob(pattern))


def get_strings_match_builder(directory: str, pattern: str):
    return StringsMatchBuilder(find_files_recursive(directory, pattern))
