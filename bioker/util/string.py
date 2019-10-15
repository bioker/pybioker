import re
from typing import List, Any, Callable, Set


def contains_match_function(string: str, patterns: Set[str]):
    return True in [pattern in string for pattern in patterns]


def regex_match_function(string: str, patterns: Set[str]):
    return None not in [re.match(pattern, str(string)) for pattern in patterns]


class StringsMatchBuilder:
    def __init__(self, strings: List[Any], match_function: Callable[[str, Set[str]], bool] = contains_match_function):
        self.strings = strings
        self.include_patterns = set()
        self.exclude_patterns = set()
        self.match_function = match_function

    def include(self, pattern):
        self.include_patterns.add(pattern)
        return self

    def exclude(self, pattern):
        self.exclude_patterns.add(pattern)
        return self

    def get_strings(self):
        result = []
        for string in self.strings:
            to_include = True
            if self.include_patterns:
                to_include = self.match_function(str(string), self.include_patterns)
            to_exclude = False
            if self.exclude_patterns:
                to_exclude = self.match_function(str(string), self.exclude_patterns)
            if to_include and not to_exclude:
                result.append(str(string))
        return result
