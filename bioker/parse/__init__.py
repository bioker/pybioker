import json

from jsonpath_ng import parse


def json_path_file(json_path: str, file_path: str) -> list:
    """
    Evaluates jsonpath expression and apply it to a content in a file.
    Returns results as a list
    """
    with open(file_path, 'r') as f:
        return json_path_obj(json_path, json.load(f))


def json_path_str(json_path: str, json_str: str) -> list:
    """
    Evaluates a jsonpath expression and apply it to a passed text.
    Returns results as a list
    """
    return json_path_obj(json_path, json.loads(json_str))


def json_path_obj(json_path: str, json_obj: dict) -> list:
    """
    Evaluates a jsonpath expression and apply it to a passed object.
    Returns results as a list
    """
    json_path_exp = parse(json_path)
    return [match.value for match in json_path_exp.find(json_obj)]
