from dataclasses import fields
from typing import Dict, Callable, Any


def set_dataclass_default_values(dataclass_obj: Any, default_value_callable_dict: Dict[str, Callable]) -> None:
    for field in fields(dataclass_obj):
        field_value = getattr(dataclass_obj, field.name, None)
        value_provider = default_value_callable_dict.get(field.name)
        if field_value is None and value_provider is not None:
            setattr(dataclass_obj, field.name, value_provider())
