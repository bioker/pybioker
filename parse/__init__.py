import json
from jsonpath_ng import parse

def json_path_file(json_path, file_path):
    with open(file_path, 'r') as f:
        return json_path_obj(json_path, json.load(f))

def json_path_str(json_path, json_str):
    return json_path_obj(json_path, json.loads(json_str))

def json_path_obj(json_path, json_obj):
    json_path_exp = parse(json_path)
    return [match.value for match in json_path_exp.find(json_obj)]
