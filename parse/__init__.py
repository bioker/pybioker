import json
from jsonpath_ng import parse

def json_path_file(json_path, file_path):
    """
    Evaluates jsonpath expression and apply it to a content in a file.
    Returns results as a list
    :param json_path - jsonpath expression
    :param file_path - file path
    :type json_path: str
    :type file_path: str
    :rtype: list
    """
    with open(file_path, 'r') as f:
        return json_path_obj(json_path, json.load(f))

def json_path_str(json_path, json_str):
    """
    Evaluates a jsonpath expression and apply it to a passed text.
    Returns results as a list
    :param json_path - jsonpath expression
    :param json_str - json string
    :type json_path: str
    :type json_str: str
    :rtype: list
    """
    return json_path_obj(json_path, json.loads(json_str))

def json_path_obj(json_path, json_obj):
    """
    Evaluates a jsonpath expression and apply it to a passed object.
    Returns results as a list
    :param json_path - jsonpath expression
    :param json_obj - json like object
    :type json_path: str
    :type json_obj: dict
    :rtype: list
    """
    json_path_exp = parse(json_path)
    return [match.value for match in json_path_exp.find(json_obj)]
