from dataclasses import fields
from typing import Any, Set, Type, TypeVar, List

T = TypeVar('T')


def dataclass_to_dict(dataclass_obj: Any, exclude: Set[str] = None):
    result = {}
    for field in fields(dataclass_obj):
        if exclude is not None and field.name in (exclude or {}):
            continue
        field_value = getattr(dataclass_obj, field.name, None)
        if field_value is not None:
            result[field.name] = field_value
    return result


def dataclass_from_dict(dataclass: Type[T], data: dict, exclude: Set[str] = None) -> T:
    args = {}
    for field in fields(dataclass):
        if field.name in data and field.name not in (exclude or {}):
            args[field.name] = data[field.name]
        else:
            args[field.name] = None
    return dataclass(**args)


def get_ids(dataclass_objects: List[T], id_field_name: str = 'id') -> List[Any]:
    return [getattr(obj, id_field_name) for obj in dataclass_objects]


def get_unique_ids(dataclass_objects: List[T], id_field_name: str = 'id') -> Set[Any]:
    return set(get_ids(dataclass_objects, id_field_name))
